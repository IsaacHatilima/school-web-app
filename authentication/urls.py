from django.urls import path
from . views import (LoginView, RequestPasswordResetView,
                     SetPasswordResetView)

urlpatterns = [
    path('', LoginView.as_view(), name="auth_login"),
    path('forgot-password/', RequestPasswordResetView.as_view(),
         name="auth_forgot_password"),
    path('set-password/', SetPasswordResetView.as_view(),
         name="auth_set_password"),
]
