from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, View):
    template_name = 'systemadmin/pages/index.html'
    login_url = '/'

    def get(self, request):
        return render(request, self.template_name)
