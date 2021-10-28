from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, TemplateView, FormView, View, RedirectView, CreateView

import stripe

from .models import Product, Category, WishlistItem, Order, OrderItem, ShippingInformation, Review
from .cart import Cart
from .forms import ShippingInformationForm, CheckoutForm, ProductReviewForm


class HomeView(ListView):
	template_name = "store/home.html"
	queryset = Product.objects.all()


class ProductDetailView(DetailView):
	template_name = "store/product_detail.html"
	model = Product

	def update_avg_rate(self):
		product = self.get_object()
		avg = 0
		rates = Review.objects.filter(product=product).values("rate")
		for value in rates:
			avg += value["rate"]
		if avg == 0:
			return avg
		return avg/len(rates)

	def get_context_data(self, **kwargs):
		context = super(ProductDetailView, self).get_context_data(**kwargs)
		item = self.get_object()
		if self.request.user.is_authenticated:
			if not self.get_object().review_set.filter(customer=self.request.user):
				orders = Order.objects.filter(customer=self.request.user)
				for order in orders:
					for orderitem in order.orderitem_set.all():
						if item == orderitem.product:
							context["review_form"] = ProductReviewForm
							break 
		return context

	def post(self, request, *args, **kwargs):
		product = self.get_object()
		form = ProductReviewForm(request.POST)
		if form.is_valid:
			review = form.save(commit=False)
			review.customer = request.user 
			review.product = self.get_object()
			review.save()
			product.rate = self.update_avg_rate()
			product.save()
		return self.get(request)


class CartView(ListView):
	template_name = "store/cart.html"

	def get_queryset(self):
		object_list = list(Cart(self.request))
		return object_list

	def get_context_data(self, **kwargs):
		context = super(CartView, self).get_context_data(**kwargs)
		context["cart"] = Cart(self.request)
		return context


class CheckoutView(LoginRequiredMixin, FormView):
	template_name = "store/checkout.html"
	form_class = CheckoutForm
	success_url = reverse_lazy("home")

	def get_form_kwargs(self):
		kwargs = super(CheckoutView, self).get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs


class ShippingInformationView(LoginRequiredMixin, FormView):
	template_name = "store/shipping_info.html"
	form_class = ShippingInformationForm

	def form_valid(self, form):
		shipping_info = form.save(commit=False)
		shipping_info.customer = self.request.user 
		shipping_info.save()
		return HttpResponseRedirect(reverse("checkout"))


class StripeCheckoutView(LoginRequiredMixin, View):
	
	def post(self, request, *args, **kwargs):
		stripe.api_key = settings.STRIPE_SECRET_KEY
		cart = request.session.get("cart")
		line_items = []

		for item in cart:
			product = Product.objects.get(pk=item)
			line_items.append({
					"name": product.title,
					"quantity": cart[item]["quantity"],
					"currency": "brl",
					"amount": int(product.price*100),
				})
		
		checkout_session = stripe.checkout.Session.create(
			payment_method_types=["card"],
			mode="payment",
			line_items=line_items,
			success_url=f"http://localhost:8000/stripe_checkout_webhook/",
			cancel_url=f"http://localhost:8000/",
			)
		
		return HttpResponseRedirect(checkout_session.url)


class OrdersHistory(ListView):
	template_name = "store/history.html"

	def get_queryset(self):
		return Order.objects.filter(customer=self.request.user)


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
def cart_add(request, pk):
	quantity = 1
	override_quantity = False

	if request.POST.get("quantity"):
		quantity = int(request.POST["quantity"])
		override_quantity = True

	cart = Cart(request)
	cart.add(pk, quantity, override_quantity)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
def cart_delete(request, pk):
	cart = Cart(request)
	cart.delete(pk)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def stripe_checkout_webhook(request):
	shipping_info = ShippingInformation.objects.filter(customer=request.user)[0]
	order = Order(customer=request.user, shipping_info=shipping_info)
	order.save()
	cart = request.session.get("cart")
		
	for item in cart:
		product = Product.objects.get(pk=item)
		OrderItem.objects.create(
				order=order, 
				product=product, 
				quantity=cart[item]["quantity"]
			)
	Cart(request).clear()
	return HttpResponseRedirect(reverse("home"))
