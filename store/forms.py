from django import forms
from .models import ShippingInformation


PAYMENT_METHODS = (
	(1, "Credit Card"),
	(2, "Debit Card")
)


class ShippingInformationForm(forms.ModelForm):

	class Meta:
		model = ShippingInformation
		exclude = ["customer"]



class CheckoutForm(forms.Form):
	payment_method = forms.ChoiceField(choices=PAYMENT_METHODS)
	
	def __init__(self, *args, **kwargs):
		user = kwargs.pop("user")
		shipping_info = ShippingInformation.objects.filter(customer=user)
		super(CheckoutForm, self).__init__(*args, **kwargs)
		self.fields["shipping_info"] = forms.ChoiceField(choices=enumerate(shipping_info))
		