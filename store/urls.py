from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/update/<int:pk>", views.update_cart, name="update_cart"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("account/", views.AccountPageView.as_view(), name="account_page"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("wishlist/<int:pk>", views.update_wishlist, name="update_wishlist"),
]
