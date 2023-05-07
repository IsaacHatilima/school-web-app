from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json
from rest_framework import status
from authentication.models import (User)


class TwoFAView(LoginRequiredMixin, View):

    def get(self, request):
        two_fa = User.objects.get(id=request.user.id)
        data = {'status': two_fa.is_two_fa}
        return HttpResponse(json.dumps(data))

    def post(self, request):
        print()
        two_fa = User.objects.get(id=request.user.id)
        state = request.POST.get('two_fa_state')
        if state == '1':
            two_fa.is_two_fa = True
        else:
            two_fa.is_two_fa = False
        two_fa.save()
        data = {'status': status.HTTP_200_OK,
                'msg': ' 2FA Updated Successfuly.'}
        return HttpResponse(json.dumps(data))
