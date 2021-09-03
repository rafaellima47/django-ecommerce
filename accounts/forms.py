from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.conf import settings
try:
	from captcha.fields import ReCaptchaField
except:
	pass 


class AccountsSignupForm(UserCreationForm):
	
	class Meta:
		model = get_user_model()
		fields = ["email"]



class AccountsLoginForm(AuthenticationForm):
	remember_me = forms.BooleanField(initial=True, required=False)

	def __init__(self, request=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if "captcha" in settings.INSTALLED_APPS:
			self.fields["captcha"] = ReCaptchaField(required=True)

