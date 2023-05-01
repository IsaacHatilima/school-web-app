from django.shortcuts import render
from django.views import View
from django.utils.html import strip_tags, escape
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Department


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

    def post(self, request):
        department = escape(strip_tags(request.POST.get('department', '')))
        dept = Department.objects.create(department=department,
                                         created_by=request.user)
        


class SettingsView(LoginRequiredMixin, View):
    template_name = 'public/settings.html'
    login_url = '/'

    def get(self, request):
        context = {
            'is_settings': True,
        }
        return render(request, self.template_name, context)
