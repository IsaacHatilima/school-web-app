from django.urls import path
from . views import (TwoFAView, EmailChecker, UsernameChecker)

urlpatterns = [
    path('two-fa/', TwoFAView.as_view(), name="get_set_two_fa"),
    path('email-checker/', EmailChecker.as_view(), name="check_email"),
    path('username-checker/', UsernameChecker.as_view(), name="check_username"),
]
