from django.urls import path
from . views import (DashboardView, SettingsView, DepartmentView,
                     DepartmentDetailsView, StaffManagerView, StaffListView)

urlpatterns = [
    path('', DashboardView.as_view(), name="admin_home"),
    path('settings/', SettingsView.as_view(), name="admin_settings"),
    path('departments/', DepartmentView.as_view(), name="admin_departments"),
    path('departments/details/<public_key>/', DepartmentDetailsView.as_view(),
         name="admin_dept_details"),
    path('users/staff/create', StaffManagerView.as_view(), name="admin_make_staff"),
    path('users/staff/list', StaffListView.as_view(), name="admin_list_staff"),
]
