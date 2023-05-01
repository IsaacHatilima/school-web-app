from django.urls import path
from . views import (TwoFAView)

urlpatterns = [
    path('two-fa/', TwoFAView.as_view(), name="get_set_two_fa"),
]
