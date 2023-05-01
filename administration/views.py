from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, View):
    template_name = 'systemadmin/pages/index.html'
    login_url = '/'

    def get(self, request):
        context = {
            'is_home': True,
        }
        return render(request, self.template_name, context)


class DepartmentView(LoginRequiredMixin, View):
    template_name = 'systemadmin/pages/departments.html'
    login_url = '/'

    def get(self, request):
        context = {
            'is_depts': True,
        }
        return render(request, self.template_name, context)


class SettingsView(LoginRequiredMixin, View):
    template_name = 'public/settings.html'
    login_url = '/'

    def get(self, request):
        context = {
            'is_settings': True,
        }
        return render(request, self.template_name, context)
