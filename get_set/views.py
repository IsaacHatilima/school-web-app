from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json
from rest_framework import status
from authentication.models import (User)


class EmailChecker(LoginRequiredMixin, View):

    def post(self, request):
        email = request.POST.get('email').lower()
        try:
            User.objects.get(email=email)
            data = {'status': status.HTTP_302_FOUND}
        except User.DoesNotExist:
            data = {'status': status.HTTP_200_OK}
        return HttpResponse(json.dumps(data))


class UsernameChecker(LoginRequiredMixin, View):

    def post(self, request):
        username = request.POST.get('username').lower()
        try:
            User.objects.get(username=username)
            data = {'status': status.HTTP_302_FOUND}
        except User.DoesNotExist:
            data = {'status': status.HTTP_200_OK}
        return HttpResponse(json.dumps(data))
