from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView, FormView, View
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Product, Category, WishlistItem
from .cart import Cart


class HomeView(ListView):
	template_name = "store/home.html"
	queryset = Product.objects.all()



class ProductDetailView(DetailView):
	template_name = "store/product_detail.html"
	model = Product



class CartView(ListView):
	template_name = "store/cart.html"

	def get_queryset(self):
		object_list = Cart(self.request)
		return object_list



class CheckoutView(FormView):
	template_name = "store/checkout.html"
	form_class = None



class AccountPageView(LoginRequiredMixin ,TemplateView):
	template_name = "store/account.html"



class SearchView(ListView):
	template_name = "store/search.html"
	model = Product
	paginate_by = 10

	def get_ordering(self, queryset, ordering):
		"""
		Return an ordered queryset according
		to the ordering option chosen
		"""
		if ordering == "1":
			pass # Highest Rate
		elif ordering == "2":
			return queryset.order_by("price")
		elif ordering == "3":
			return queryset.order_by("-price")
		elif ordering == "4":
			return queryset.order_by("-created")
		return queryset

	def get_queryset(self):
		"""
		Return the filtered queryset
		"""
		s = self.request.GET.get("s")
		categories = self.request.GET.getlist("category")
		ordering = self.request.GET.get("order")

		if s:
			object_list = self.model.objects.filter(title__icontains=s)
		else:
			object_list = self.model.objects.all()

		if categories:
			for category in categories:
				object_list = object_list.filter(category__title=category)

		if ordering:
			object_list = self.get_ordering(object_list, ordering)

		return object_list

	def get_context_data(self, **kwargs):
		context = super(SearchView, self).get_context_data(**kwargs)
		context["categories_list"] = Category.objects.all()
		return context



@login_required
def update_wishlist(request, pk):
	customer = request.user
	product = get_object_or_404(Product, pk=pk)

	try:
		item = WishlistItem.objects.get(customer=customer, product=product)
		item.delete()
	except WishlistItem.DoesNotExist:
		item = WishlistItem(customer=customer, product=product)
		item.save()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



@require_POST
def update_cart(request, pk, quantity=1, method=None):
	cart = Cart(request)

	if method == "add":
		cart.add(pk, quantity)
	elif method == "delete":
		cart.delete(pk)

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

