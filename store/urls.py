from django.urls import path

from . import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/add/<int:pk>", views.cart_add, name="cart_add"),
    path("cart/delete/<int:pk>", views.cart_delete, name="cart_delete"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("shipping-information/", views.ShippingInformationView.as_view(), name="shipping_info"),
    path("stripe/create-checkout-session", views.StripeCheckoutView.as_view(), name="stripe_checkout"),
    path("stripe_checkout_webhook/", views.stripe_checkout_webhook, name="stripe_checkout_webhook"),
    path("account/orders_history/", views.OrdersHistory.as_view(), name="orders_history"),
    path("account/", views.AccountPageView.as_view(), name="account_page"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("wishlist/<int:pk>", views.update_wishlist, name="update_wishlist"),
]
