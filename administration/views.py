import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.utils.html import strip_tags, escape
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string
from authentication.models import User, Profile


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
        context = {
            'is_makeStaff': True,
            'user_roles': User.ROLE_CHOICES
        }
        return render(request, self.template_name, context)

    def post(self, request):
        first_name = escape(strip_tags(request.POST.get('fname', '')))
        last_name = escape(strip_tags(request.POST.get('lname', '')))
        email = escape(strip_tags(request.POST.get('email', ''))).lower()
        cell = escape(strip_tags(request.POST.get('cell', '')))
        username = escape(strip_tags(request.POST.get('username', '')))
        marital_status = escape(strip_tags(request.POST.get('marital_status', '')))
        role = escape(strip_tags(request.POST.get('role', '')))
        password = get_random_string(length=8)
        # Create User Profile
        prof, created = Profile.objects.get_or_create(firstname=first_name,
                                                      lastname=last_name,
                                                      cell=cell,
                                                      marital_status=marital_status)
        if created:
            # Create Profile
            user = User.objects.create_user(username=username, email=email, role=role,
                                            profile=prof,
                                            password=password)
            if user:
                data = {'status': status.HTTP_201_CREATED,
                        'msg': prof.firstname+'`s Account Created Successfuly.'}
            else:
                data = {'status': status.HTTP_400_BAD_REQUEST,
                        'msg': 'Unable To Create Account.'}
        else:
            data = {'status': status.HTTP_400_BAD_REQUEST,
                    'msg': 'Unable To Create Account.'}
        return HttpResponse(json.dumps(data))


# class StaffListView(LoginRequiredMixin, View):
#     template_name = 'systemadmin/pages/staffList.html'
#     login_url = '/'
#     redirect_field_name = 'next'

#     def get(self, request):
#         # instance = StaffProfile.objects.all()
#         context = {
#             'is_listStaff': True,
#             'staff': 'instance',
#         }
#         return render(request, self.template_name, context)


# class StaffUpdateView(LoginRequiredMixin, View):
#     template_name = 'systemadmin/pages/updateStaff.html'
#     login_url = '/'
#     redirect_field_name = 'next'

#     def get(self, request, public_key):
#         instance = StaffProfile.objects.get(public_key=public_key)
#         dept = Department.objects.all()
#         context = {
#             'is_listStaff': True,
#             'staff': instance,
#             'dept': dept
#         }
#         return render(request, self.template_name, context)

#     def post(self, request, public_key):
#         public_key = escape(strip_tags(request.POST.get('user_id', '')))
#         first_name = escape(strip_tags(request.POST.get('fname', '')))
#         last_name = escape(strip_tags(request.POST.get('lname', '')))
#         cell = escape(strip_tags(request.POST.get('cell', '')))
#         marital_status = escape(strip_tags(request.POST.get('marital_status', '')))
#         dept = escape(strip_tags(request.POST.get('department', '')))
#         role = escape(strip_tags(request.POST.get('role', '')))
#         try:
#             profile = StaffProfile.objects.get(public_key=public_key)
#             profile.firstname = first_name
#             profile.last_name = last_name
#             profile.cell = cell
#             profile.marital_status = marital_status
#             profile.dept = dept
#             profile.role = role
#             profile.save()
#             data = {'status': status.HTTP_200_OK,
#                     'msg': 'Account Updated Successfuly.'}
#         except StaffProfile.DoesNotExist:
#             data = {'status': status.HTTP_404_NOT_FOUND,
#                     'msg': 'Account Not Found.'}
#         return HttpResponse(json.dumps(data))
