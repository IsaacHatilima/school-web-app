from django.urls import path
from . views import (DashboardView, SettingsView, StaffManagerView, StaffListView, StaffUpdateView)

urlpatterns = [
    path('', DashboardView.as_view(), name="admin_home"),
    path('settings/', SettingsView.as_view(), name="admin_settings"),
    path('users/staff/create', StaffManagerView.as_view(), name="admin_make_staff"),
    path('users/staff/list', StaffListView.as_view(), name="admin_list_staff"),
    path("users/staff/update/<public_key>/", StaffUpdateView.as_view(),
         name="admin_staff_update"),
]
