from django.urls import path
from . views import (LoginView, RequestPasswordResetView)

urlpatterns = [
    path('', LoginView.as_view(), name="auth_login"),
    path('forgot-password/', RequestPasswordResetView.as_view(),
         name="auth_forgotpassword"),
]
