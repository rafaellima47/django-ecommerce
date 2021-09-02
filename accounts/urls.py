from django.urls import path, include
from . import views

urlpatterns = [
    path("signup/", views.AccountsSignupView.as_view(), name="signup"),
    path("login/", views.AccountsLoginView.as_view(), name='login'),
    path("logout/", views.AccountsLogoutView.as_view(), name='logout'),
    path("password_reset/", views.AccountsPasswordResetView.as_view(), name='password_reset'),
    path("password_change/", views.AccountsPasswordChangeView.as_view(), name='password_change'),
    path("password_change/done/", views.AccountsPasswordChangeDoneView.as_view(), name='password_change_done'),
    path("password_reset/<uidb64>/<token>/", views.AccountsPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("password_reset/done/", views.AccountsPasswordResetDoneView.as_view(), name='password_reset_done'),
    path("reset/done/", views.AccountsPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # social_django URL's
    path('oauth/', include('social_django.urls', namespace="social")),
]