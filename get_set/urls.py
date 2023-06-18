from django.urls import path
from . views import (EmailChecker, UsernameChecker)

urlpatterns = [
    path('email-checker/', EmailChecker.as_view(), name="check_email"),
    path('username-checker/', UsernameChecker.as_view(), name="check_username"),
]
