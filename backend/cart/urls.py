from django.urls import path
from .views import CartView, UpdateCartItemView, RemoveFromCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/<int:item_id>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    # RemoveFromCartView is not needed separately, handled by UpdateCartItemView with DELETE method
] 