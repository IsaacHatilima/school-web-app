from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import get_template
from django.core.mail import EmailMessage
import os
from django.conf import settings
import datetime
from django.urls import reverse
from authentication.models import User


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(id=instance.id)
        TokenLifeTime = datetime.timedelta(minutes=30)
        if user:
            token = RefreshToken.for_user(user).access_token
            token.set_exp(lifetime=TokenLifeTime)
            absurl = os.environ['APP_URL']+reverse('auth_set_password')+"?token="+str(token)
            htmly = get_template('emailTemplates/verifyAccount.html')
            context = {'firstname': instance.profile.firstname,
                       'username': instance.username,
                       'email': instance.email,
                       'absurl': absurl}
            html_content = htmly.render(context)
            msg = EmailMessage(subject='Account Verification',
                               body=html_content,
                               to=[user.email],
                               from_email=settings.DEFAULT_FROM_EMAIL)
            msg.content_subtype = 'html'
            msg.send()
