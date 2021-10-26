from rest_framework.viewsets import ModelViewSet 

from .serializers import ProductsSerializer
from store.models import Product


class ProductsViewSet(ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductsSerializer
