from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator


class Base(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Category(Base):
	title = models.CharField(max_length=200)

	def __str__(self):
		return self.title


class Product(Base):
	title = models.CharField(max_length=200)
	description = models.TextField()
	price = models.FloatField()
	is_digital = models.BooleanField(default=False)
	category = models.ManyToManyField(Category)

	def __str__(self):
		return self.title


class ProductImage(Base):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="images/", default=None)

	def __str__(self):
		return str(self.id)


class ShippingInformation(Base):
	customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	address = models.CharField(max_length=300)
	city =  models.CharField(max_length=300)
	state =  models.CharField(max_length=300)
	zipcode = models.CharField(max_length=300)

	def __str__(self):
		return self.address


class Order(Base):
	customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	shipping_info = models.ForeignKey(ShippingInformation, on_delete=models.CASCADE)
	complete = models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)


class OrderItem(Base):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.product


class Review(Base):
	customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	rate = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
	review = models.TextField()

	def __str__(self):
		return str(self.id)

	class Meta:
		unique_together = ["customer", "product"]


class WishlistItem(Base):
	customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
