from django.urls import path
from . views import (LoginView, RequestPasswordResetView,
                     SetPasswordResetView, TwoFAView, LogoutView)

urlpatterns = [
    path('', LoginView.as_view(), name="auth_login"),
    path('logout/', LogoutView.as_view(), name="auth_logout"),
    path('login-verification/', TwoFAView.as_view(), name="auth_two_fa"),
    path('forgot-password/', RequestPasswordResetView.as_view(),
         name="auth_forgot_password"),
    path('set-password/', SetPasswordResetView.as_view(),
         name="auth_set_password"),
]
