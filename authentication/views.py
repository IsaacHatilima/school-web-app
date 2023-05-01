from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login as auth_login
from django.utils.html import strip_tags, escape
from django.conf import settings
from rest_framework import status
import json
from django.urls import reverse
from django.utils.crypto import get_random_string
from .utils import Util
from django.template.loader import get_template
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
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
        password = escape(strip_tags(request.POST.get('password', '')))
        # Check if 2FA is ACTIVE
        # 2FA IS NOT ACTIVE
        if not validUser.is_two_fa:
            if validUser.is_active:
                if validUser.is_verified:
                    auth_login(request, validUser)
                    remember = request.POST.get('remember_me')
                    if remember:
                        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                    else:
                        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                    data = {
                        'status': status.HTTP_200_OK,
                        'msg': 'Login Successful.',
                        'login_type': 'No 2FA',
                        'destination': reverse('admin_home'),
                        'url': request.POST.get('next')
                    }
                else:
                    data = {'status': status.HTTP_401_UNAUTHORIZED,
                            'msg': 'Your account is not verified.'}
            else:
                data = {'status': status.HTTP_401_UNAUTHORIZED,
                        'msg': 'Your account has been disabled.'}
        # 2FA IS ACTIVE
        else:
            if validUser.check_password(password):
                request.session['email'] = validUser.email
                remember = request.POST.get('remember_me')
                request.session['next'] = request.POST.get('next', '')
                if remember:
                    request.session['remember_me'] = request.POST.get(
                        'remember_me', '')
                else:
                    request.session['remember_me'] = request.POST.get(
                        'remember_me', '')
                # Send 2FA Code
                two_fa = get_random_string(length=6)
                # Store Code
                validUser.two_fa = two_fa.upper()
                validUser.save()
                # Email Code
                htmly = get_template('emailTemplates/2fa.html')
                context = {'firstname': validUser.username,
                           "code": two_fa.upper()}
                html_content = htmly.render(context)
                data = {
                    'email_to': validUser.email,
                    'email_body': html_content,
                    'email_subject': '2FA Code'
                }
                Util.send_email(data)
                # Return Success
                data = {'status': status.HTTP_200_OK,
                        'msg': 'Valid User.'}
            else:
                data = {'status': status.HTTP_403_FORBIDDEN,
                        'msg': 'Invalid Email or Password.'}
        return HttpResponse(json.dumps(data))


class TwoFAView(View):
    template_name = 'auth/twofa.html'

    def get(self, request):
        remember_me = request.session.get('remember_me')
        next_url = request.session.get('next')
        context = {"remember_me": remember_me, "next_url": next_url}
        return render(request, self.template_name, context)

    def post(self, request, format=None):
        two_fa_code = escape(strip_tags(request.POST.get('auth_code', '')))
        validUser = User.objects.get(two_fa=two_fa_code,
                                     email=request.session.get('email'))
        if validUser:
            if validUser.is_active:
                if validUser.is_verified:
                    auth_login(request, validUser)
                    remember = request.POST.get('remember_me')
                    if remember:
                        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                    else:
                        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                    data = {
                        'status': status.HTTP_200_OK,
                        'msg': 'Login Successful.',
                        'login_type': 'With 2FA',
                        'destination': reverse('admin_home'),
                        'url': request.POST.get('next')
                    }
                    validUser.two_fa = ''
                    validUser.save()
                    del request.session['email']
                    del request.session['remember_me']
                    del request.session['next']
                else:
                    data = {'status': status.HTTP_401_UNAUTHORIZED,
                            'msg': 'Your account is not verified.'}
            else:
                data = {'status': status.HTTP_401_UNAUTHORIZED,
                        'msg': 'Your account has been disabled.'}
        else:
            data = {'status': status.HTTP_403_FORBIDDEN,
                    'msg': 'Invalid Code.'}
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
                token = RefreshToken.for_user(associated_users).access_token
                current_site = get_current_site(request).domain
                relative_link = reverse('auth_set_password')
                absurl = 'http://'+current_site
                + relative_link+"?token="+str(token)
                htmly = get_template('email/newPassword.html')
                context = {'firstname': associated_users.firstname+' '
                           + associated_users.lastname, "absurl": absurl}
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
            data = {'status': status.HTTP_200_OK,
                    'msg': 'An email has been sent to you email.'}
        return HttpResponse(json.dumps(data))


class SetPasswordResetView(View):
    template_name = 'auth/setPassword.html'

    def get(self, request):
        return render(request, self.template_name)
