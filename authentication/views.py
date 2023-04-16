from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.utils.html import strip_tags, escape
from django.conf import settings
from rest_framework import status
import json
from django.urls import reverse
from .models import User


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('auth_login'))


class LoginView(View):
    template_name = 'auth/index.html'

    def get(self, request):
        return render(request, self.template_name)
        # if request.user.is_authenticated:
        #     if request.user.role == 'System Admin':
        #         return HttpResponseRedirect(reverse('admin_home'))
        # else:
        #     return render(request, self.template_name)

    def post(self, request, format=None):
        username_email = escape(strip_tags(request.POST.get('email', '')))
        if '@' in username_email:
            email = username_email
        else:
            validUser = User.objects.get(username=username_email)
            email = validUser.email
        password = escape(strip_tags(request.POST.get('password', '')))
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                if user.is_verified:
                    auth_login(request, user)
                    remember = escape(strip_tags(
                        request.POST.get('remember_me', '')))
                    if remember:
                        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
                    else:
                        settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                    data = {
                        'status': status.HTTP_200_OK,
                        'msg': 'Login Successful.',
                        'role': user.role,
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


class SetPasswordResetView(View):
    template_name = 'auth/setPassword.html'

    def get(self, request):
        return render(request, self.template_name)
