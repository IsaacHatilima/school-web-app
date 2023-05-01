from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import json
from authentication.models import (User)


class TwoFAView(LoginRequiredMixin, View):

    def get(self, request):
        two_fa = User.objects.get(id=request.user.id)
        data = {'status': two_fa.is_two_fa}
        return HttpResponse(json.dumps(data))
