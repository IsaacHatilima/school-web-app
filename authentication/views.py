from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.utils.html import strip_tags, escape
from django.conf import settings
from rest_framework import status
import json
from django.urls import reverse
from .utils import Util
from django.template.loader import get_template
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
import jwt
import datetime
from .models import User


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('auth_login'))


class LoginView(View):
    template_name = 'auth/index.html'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.role == 'System Admin':
                return HttpResponseRedirect(reverse('admin_home'))
        else:
            return render(request, self.template_name)

    def post(self, request, format=None):
        username_email = escape(strip_tags(request.POST.get('email', '')))
        if '@' in username_email:
            validUser = User.objects.get(email=username_email)
        else:
            validUser = User.objects.get(username=username_email)
        user = authenticate(email=validUser.email,
                            password=escape(strip_tags(request.POST.get('password', ''))))
        if user:
            if user.is_active:
                if user.is_verified:
                    auth_login(request, user)
                    remember = escape(strip_tags(request.POST.get('remember_me', '')))
                    if remember:
                        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                    else:
                        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                    if user.role == 'System Admin':
                        url = reverse('admin_home')
                    data = {
                        'status': status.HTTP_200_OK,
                        'msg': 'Login Successful.',
                        'role': user.role,
                        'destination': url,
                    }
                else:
                    data = {'status': status.HTTP_401_UNAUTHORIZED,
                            'msg': 'Your account is not verified.'}
            else:
                data = {'status': status.HTTP_401_UNAUTHORIZED,
                        'msg': 'Your account has been disabled.'}
        else:
            data = {'status': status.HTTP_403_FORBIDDEN,
                    'msg': 'Invalid Email or Password.'}
        return HttpResponse(json.dumps(data))


class RequestPasswordResetView(View):
    template_name = 'auth/forgotPassword.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, format=None):
        try:
            associated_users = User.objects.get(
                email=escape(strip_tags(request.POST.get('email', ''))))
            if associated_users:
                TokenLifeTime = datetime.timedelta(minutes=30)
                token = RefreshToken.for_user(associated_users).access_token
                token.set_exp(lifetime=TokenLifeTime)
                current_site = get_current_site(request).domain
                relative_link = reverse('auth_set_password')
                absurl = 'http://'+current_site+relative_link+"?token="+str(token)
                htmly = get_template('emailTemplates/newPassword.html')
                context = {'firstname': associated_users.profile.firstname+' '
                           + associated_users.profile.lastname, "absurl": absurl}
                html_content = htmly.render(context)
                data = {
                    'email_to': associated_users.email,
                    'email_body': html_content,
                    'email_subject': 'Password Reset'
                }
                Util.send_email(data)
                data = {'status': status.HTTP_200_OK,
                        'msg': 'An email has been sent to you email.'}
        except User.DoesNotExist:
            data = {'status': status.HTTP_400_BAD_REQUEST,
                    'msg': 'An email has been sent to you email.'}
        return HttpResponse(json.dumps(data))


class SetPasswordResetView(View):
    template_name = 'auth/setPassword.html'
    error_template = 'auth/setPassTokenError.html'

    def get(self, request):
        token = request.GET.get('token')
        try:
            jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            return render(request, self.template_name)
        except jwt.ExpiredSignatureError:
            return render(request, self.error_template, context={'message': 'Token Has Expired'})
        except jwt.exceptions.DecodeError:
            return render(request, self.error_template, context={'message': 'Invalid Token'})

    def post(self, request, format=None):
        try:
            token = request.POST.get('token')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            # Change Password
            associated_users = User.objects.get(id=payload['user_id'])
            associated_users.is_verified = True
            associated_users.set_password(escape(strip_tags(request.POST.get('password', ''))))
            associated_users.save()
            data = {'status': status.HTTP_200_OK, 'msg': 'Password Changed, Redirecting.'}
            return HttpResponse(json.dumps(data))
        except jwt.ExpiredSignatureError:
            data = {'status': status.HTTP_401_UNAUTHORIZED, 'msg': 'Token Has Expired.'}
            return HttpResponse(json.dumps(data))
        except jwt.exceptions.DecodeError:
            data = {'status': status.HTTP_401_UNAUTHORIZED,
                    'msg': 'Invalid Token.'}
            return HttpResponse(json.dumps(data))
