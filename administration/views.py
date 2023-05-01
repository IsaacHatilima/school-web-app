import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils.html import strip_tags, escape
from rest_framework import status
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
        instance = Department.objects.all()
        context = {
            'is_depts': True,
            'depts': instance,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        department = escape(strip_tags(request.POST.get('department', '')))
        try:
            Department.objects.get(department=department.capitalize())
            data = {'status': status.HTTP_302_FOUND,
                    'msg': 'Department Already Exists.'}
        except Department.DoesNotExist:
            Department.objects.create(department=department,
                                      created_by=request.user)
            data = {'status': status.HTTP_201_CREATED,
                    'msg': 'Department Created Successfuly.'}
        return HttpResponse(json.dumps(data))


class DepartmentDetailsView(LoginRequiredMixin, View):

    def get(self, request):
        pass


class SettingsView(LoginRequiredMixin, View):
    template_name = 'public/settings.html'
    login_url = '/'

    def get(self, request):
        context = {
            'is_settings': True,
        }
        return render(request, self.template_name, context)
