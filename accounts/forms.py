from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.conf import settings
try:
	from captcha.fields import ReCaptchaField
except:
	pass 


class AccountsSignupForm(UserCreationForm):
	captcha = ReCaptchaField(required=True)
	
	class Meta:
		model = get_user_model()
		fields = ["email"]


class AccountsLoginForm(AuthenticationForm):
	remember_me = forms.BooleanField(initial=True, required=False)
	captcha = ReCaptchaField(required=True)

