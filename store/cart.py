from .models import Product


class Cart(object):

	def __init__(self, request):
		if not request.session.get("cart"):
			request.session["cart"] = {}

		self.session = request.session
		self.cart = request.session["cart"]

	def __iter__(self):
		for product_id in self.cart:
			yield {"product": Product.objects.get(pk=product_id),
					"quantity": self.cart[product_id]["quantity"],
					}

	def add(self, product_id, quantity, override_quantity):
		product_id = str(product_id)

		if product_id not in self.cart:
			self.cart[product_id] = {"quantity": quantity}
		else:
			if override_quantity:
				self.cart[product_id]["quantity"] = quantity
			else:
				self.cart[product_id]["quantity"] += quantity

		self.session.modified = True

	def delete(self, product_id=None, clear=False):
		product_id = str(product_id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.session.modified = True

	def clear(self):
		print("CLEAAAR")
		del self.session["cart"]
		self.session.modified = True

	@property
	def get_total(self):
		total = 0
		for product_id in self.cart:
			total += Product.objects.get(pk=product_id).price * self.cart[product_id]["quantity"]
		return total