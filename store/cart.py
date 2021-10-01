from .models import Product


class Cart(object):

	def __init__(self, request):
		if not request.session.get("cart"):
			request.session["cart"] = {}

		self.session = request.session
		self.cart = request.session["cart"]

	def __iter__(self):
		print("iter")
		for product_id in self.cart:
			print("ala")
			yield Product.objects.get(pk=product_id)

	def add(self, product_id, quantity):
		product_id = str(product_id)

		if product_id not in self.cart:
			self.cart[product_id] = {"quantity": quantity}
		else:
			self.cart[product_id]["quantity"] += quantity

		self.session.modified = True

	def delete(self, product_id):
		product_id = str(product_id)

		if product_id in self.cart:
			del self.cart[product_id]
			self.session.modified = True