from django.urls import path
from . views import (DashboardView, SettingsView, DepartmentView,
                     DepartmentDetailsView)

urlpatterns = [
    path('', DashboardView.as_view(), name="admin_home"),
    path('settings/', SettingsView.as_view(), name="admin_settings"),
    path('departments/', DepartmentView.as_view(), name="admin_departments"),
    path('departments/details/<public_key>/', DepartmentDetailsView.as_view(),
         name="admin_dept_details"),
]
