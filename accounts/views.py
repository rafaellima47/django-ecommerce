from django.views.generic import CreateView
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.encoding import force_bytes, force_text  
from django.contrib.auth import get_user_model
from django.contrib import messages
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

from .forms import AccountsSignupForm, AccountsLoginForm
from .tokens import TokenGenerator


class AccountsSignupView(CreateView):
	template_name = "accounts/signup.html"
	form_class = AccountsSignupForm
	success_url = reverse_lazy(settings.LOGIN_URL)

	def send_activation_email(self, user):
		current_site = get_current_site(self.request)  
		template = render_to_string("accounts/activation_template.html", {
			"domain": current_site.domain,
			"uid": urlsafe_base64_encode(force_bytes(user.pk)),  
			"token": TokenGenerator().make_token(user),
			})
		email = EmailMessage("Account Activation",template,settings.EMAIL_HOST_USER,[user.email])
		email.send()
		
	def get(self, request, *args, **kwargs):
		'''	
		If user is authenticated redirect to LOGIN_REDIRECT_URL
		'''
		if request.user.is_authenticated:
			return HttpResponseRedirect(self.get_success_url())
		return super(AccountsSignupView, self).get(request, *args, **kwargs)
	
	def form_valid(self, form):
		'''
		If the user creation is successful, login the new user and redirects to homepage
		'''
		valid = super(AccountsSignupView, self).form_valid(form)
		email, password = form.cleaned_data.get("email"), form.cleaned_data.get("password1")
		user = authenticate(email=email, password=password)
		user.is_active = False
		user.save()
		try:
			self.send_activation_email(user)
		except:
			pass 
		return valid


def activate(request, uidb64, token):
	User = get_user_model()  
	try:  
		uid = force_text(urlsafe_base64_decode(uidb64))  
		user = User.objects.get(pk=uid)  
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
		user = None
	if user is not None and TokenGenerator().check_token(user, token):  
		user.is_active = True  
		user.save()  
		messages.success(request, "You can now login to your account")
	else:  
		messages.success(request, "Invalid")
	return HttpResponseRedirect(reverse("login"))


class AccountsLoginView(LoginView):
	template_name = "accounts/login.html"
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
