from django.urls import path, include
from django.conf import settings 

from . import views

urlpatterns = [
    path("signup/", views.AccountsSignupView.as_view(), name="signup"),
    path("activation/<uidb64>/<token>/", views.activate, name="activation"),
    path("login/", views.AccountsLoginView.as_view(), name='login'),
    path("logout/", views.AccountsLogoutView.as_view(), name='logout'),
    path("password_reset/", views.AccountsPasswordResetView.as_view(), name='password_reset'),
    path("password_change/", views.AccountsPasswordChangeView.as_view(), name='password_change'),
    path("password_change/done/", views.AccountsPasswordChangeDoneView.as_view(), name='password_change_done'),
    path("password_reset/<uidb64>/<token>/", views.AccountsPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("password_reset/done/", views.AccountsPasswordResetDoneView.as_view(), name='password_reset_done'),
    path("reset/done/", views.AccountsPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

# If social_django is installed adds it to the urlpatterns
if "social_django" in settings.INSTALLED_APPS:
    urlpatterns += [path("oauth/", include("social_django.urls", namespace="social"))]