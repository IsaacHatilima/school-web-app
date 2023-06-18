from django.urls import path
from . views import (LoginView, RequestPasswordResetView,
                     SetPasswordResetView, LogoutView, UpdatePasswordView)

urlpatterns = [
    path('', LoginView.as_view(), name="auth_login"),
    path('logout/', LogoutView.as_view(), name="auth_logout"),
    path('forgot-password/', RequestPasswordResetView.as_view(),
         name="auth_forgot_password"),
    path('set-password/', SetPasswordResetView.as_view(),
         name="auth_set_password"),
    path('password-update/', UpdatePasswordView.as_view(), name="auth_pass_update"),
]
