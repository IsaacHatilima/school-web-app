from django.urls import path
from . views import (DashboardView, SettingsView)

urlpatterns = [
    path('', DashboardView.as_view(), name="admin_home"),
    path('settings/', SettingsView.as_view(), name="admin_settings"),
]
