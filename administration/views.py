import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils.html import strip_tags, escape
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from authentication.models import User, StaffProfile
from authentication.permissions import get_staff_id
from .models import Department


class DashboardView(LoginRequiredMixin, View):
    template_name = 'systemadmin/pages/index.html'
    login_url = '/'
    redirect_field_name = 'next'

    def get(self, request):
        context = {
            'is_home': True,
        }
        return render(request, self.template_name, context)


def page_not_found(request, exception):
    return render(request, '404.html')


class DepartmentView(LoginRequiredMixin, View):
    template_name = 'systemadmin/pages/departments.html'
    login_url = '/'
    redirect_field_name = 'next'

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
            Department.objects.get(department=department.title())
            data = {'status': status.HTTP_302_FOUND,
                    'msg': 'Department Already Exists.'}
        except Department.DoesNotExist:
            # print(get_staff_id(request))
            Department.objects.create(department=department.title(),
                                      created_by=get_staff_id(request))
            data = {'status': status.HTTP_201_CREATED,
                    'msg': department.title()+' Department Created Successfuly.'}
        return HttpResponse(json.dumps(data))


class DepartmentDetailsView(LoginRequiredMixin, View):

    def post(self, request, public_key):
        department = escape(strip_tags(request.POST.get('department', '')))
        instance = Department.objects.get(public_key=public_key)
        instance.department = department.title()
        instance.save()
        data = {'status': status.HTTP_200_OK,
                'msg': department.title()+' Department Updated Successfuly.'}
        return HttpResponse(json.dumps(data))

    def delete(self, request, public_key):
        department = escape(strip_tags(request.POST.get('department', '')))
        instance = Department.objects.get(public_key=public_key)
        instance.delete()
        data = {'status': status.HTTP_200_OK,
                'msg': department.title()+' Department Deleted Successfuly.'}
        return HttpResponse(json.dumps(data))


class SettingsView(LoginRequiredMixin, View):
    template_name = 'public/settings.html'
    login_url = '/'
    redirect_field_name = 'next'

    def get(self, request):
        two_fa = User.objects.get(id=request.user.id)
        if two_fa.is_two_fa:
            auth_state = 'checked'
        else:
            auth_state = ''
        context = {
            'is_settings': True,
            'two_fa': auth_state
        }
        return render(request, self.template_name, context)


class StaffManagerView(LoginRequiredMixin, View):
    template_name = 'systemadmin/pages/createStaff.html'
    login_url = '/'
    redirect_field_name = 'next'

    def get(self, request):
        instance = Department.objects.all()
        context = {
            'is_makeStaff': True,
            'departments': instance
        }
        return render(request, self.template_name, context)

    def post(self, request):
        first_name = escape(strip_tags(request.POST.get('fname', '')))
        last_name = escape(strip_tags(request.POST.get('lname', '')))
        email = escape(strip_tags(request.POST.get('email', ''))).lower()
        cell = escape(strip_tags(request.POST.get('cell', '')))
        username = escape(strip_tags(request.POST.get('username', '')))
        marital_status = escape(strip_tags(request.POST.get('marital_status', '')))
        dept = escape(strip_tags(request.POST.get('department', '')))
        role = escape(strip_tags(request.POST.get('role', '')))
        password = get_random_string(length=8)
        # Create User
        user = User.objects.create_user(username=username, email=email, role=role,
                                        password=password)
        # Get Department
        department = Department.objects.get(public_key=dept)
        # Create Profile
        StaffProfile.objects.create(firstname=first_name, lastname=last_name,
                                    cell=cell, marital_status=marital_status,
                                    user=user, department_of=department)
        # Increment Department Count
        department.members = department.members+1
        department.save()
        data = {'status': status.HTTP_201_CREATED,
                'msg': 'Account Created Successfuly.'}
        return HttpResponse(json.dumps(data))
