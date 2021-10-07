from django.views.generic import CreateView, TemplateView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import AccountsSignupForm, AccountsLoginForm
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.encoding import force_bytes, force_text  
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
	template_name = "accounts/signup.html"
	form_class = AccountsSignupForm
	success_url = settings.LOGIN_URL

	def send_activation_email(self, user):
		current_site = get_current_site(self.request)  
		template = render_to_string("accounts/activation_template.html", {
			"domain": current_site.domain,
			"uid": urlsafe_base64_encode(force_bytes(user.pk)),  
			"token": TokenGenerator().make_token(user),
			})

		email = EmailMessage(
			"Account Activation",
			template,
			settings.EMAIL_HOST_USER,
			[user.email]
			)
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
		self.send_activation_email(user)
		return valid




class AccountActivationView(TemplateView):
	template_name = "accounts/activation.html"

	def get_context_data(self, **kwargs):
		context = super(AccountActivationView, self).get_context_data(**kwargs)
		context["email"] = kwargs.get("email")
		return context

	def post(self, request, *args, **kwargs):
		template = render_to_string("accounts/activation_template.html")
		email = EmailMessage(
			"Account Activation",
			template,
			settings.EMAIL_HOST_USER,
			["47rafael.lima@gmail.com"]
			)
		email.send()
		return HttpResponseRedirect("")



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
