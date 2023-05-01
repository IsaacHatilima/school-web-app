from django.core.mail import EmailMessage
from django.conf import settings


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'],
            to=[data['email_to']], from_email=settings.DEFAULT_FROM_EMAIL)
        email.content_subtype = "html"
        email.send()
