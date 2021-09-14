from django.views.generic import ListView, DetailView, TemplateView, FormView

from .models import Product


class HomeView(ListView):
	template_name = "store/home.html"
	queryset = Product.objects.all()



class ProductDetailView(DetailView):
	template_name = "store/product_detail.html"
	queryset = Product.objects.all()



class CartView(TemplateView):
	template_name = "store/cart.html"



class CheckoutView(FormView):
	template_name = "store/checkout.html"
	form_class = None
