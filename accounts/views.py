from django.views.generic import CreateView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import AccountsSignupForm, AccountsLoginForm
from django.conf import settings
from django.contrib.auth.views import (
	LoginView,
	LogoutView,
	PasswordResetView,
	PasswordChangeView,
	PasswordChangeDoneView,
	PasswordResetConfirmView,
	PasswordResetDoneView,
	PasswordResetCompleteView,
	)


class AccountsSignupView(CreateView):
	template_name = "registration/signup.html"
	form_class = AccountsSignupForm
	success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
	
	def get(self, request, *args, **kwargs):
		'''	
		If user is authenticated redirect to LOGIN_REDIRECT_URL
		'''
		if request.user.is_authenticated:
			return HttpResponseRedirect(self.success_url)
		return super(AccountsSignupView, self).get(request, *args, **kwargs)
	
	def form_valid(self, form):
		'''
		If the user creation is successful, login the new user and redirects to homepage
		'''
		valid = super(AccountsSignupView, self).form_valid(form)
		email, password = form.cleaned_data.get("email"), form.cleaned_data.get("password1")
		user = authenticate(email=email, password=password)
		login(self.request, user)
		return valid



class AccountsLoginView(LoginView):
	form_class = AccountsLoginForm
	redirect_authenticated_user = True

	def form_valid(self, form):
		'''
		Changes the session timeout according to the remember_me checkbox value
		'''
		if not form.cleaned_data.get("remember_me"):
			self.request.session.set_expiry(0)
		login(self.request, form.get_user())
		return HttpResponseRedirect(self.get_success_url())



class AccountsLogoutView(LogoutView):
	pass



class AccountsPasswordChangeView(PasswordChangeView):
	pass



class AccountsPasswordChangeDoneView(PasswordChangeDoneView):
	pass



class AccountsPasswordResetView(PasswordResetView):
	pass



class AccountsPasswordResetConfirmView(PasswordResetConfirmView):
	pass



class AccountsPasswordResetDoneView(PasswordResetDoneView):
	pass



class AccountsPasswordResetCompleteView(PasswordResetCompleteView):
	pass
