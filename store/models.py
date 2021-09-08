from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator


class Base(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True



class Product(Base):
	title = models.CharField(max_length=200)
	description = models.TextField()
	price = models.FloatField()
	is_digital = models.BooleanField(default=False)
	#images = None

	def __str__(self):
		return self.title



class Review(Base):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	rate = models.PositiveIntegerField(validators=[MaxValueValidator(5)])
	Review = models.TextField()

	class Meta:
		unique_together = ["user", "product"]
