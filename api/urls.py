from rest_framework.routers import SimpleRouter

from .views import ProductsViewSet


router = SimpleRouter()
router.register("products", ProductsViewSet)