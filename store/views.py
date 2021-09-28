from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView, FormView, View

from .models import Product


class HomeView(ListView):
	template_name = "store/home.html"
	queryset = Product.objects.all()



class ProductDetailView(DetailView):
	template_name = "store/product_detail.html"
	model = Product



class CartView(TemplateView):
	template_name = "store/cart.html"



class CheckoutView(FormView):
	template_name = "store/checkout.html"
	form_class = None



class AccountPageView(LoginRequiredMixin ,TemplateView):
	template_name = "store/account.html"



class SearchView(ListView):
	template_name = "store/search.html"
	model = Product

	def get_queryset(self):
		s = self.request.GET.get("s")
		print(s)
		if s:
			object_list = self.model.objects.filter(title__icontains=s)
		else:
			object_list = self.model.objects.all()
		return object_list