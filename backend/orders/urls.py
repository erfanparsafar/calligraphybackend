from django.urls import path
from .views import OrderListView, UserOrderListView, OrderCreateView, OrderDetailView, OrderStatusUpdateView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='admin_orders'),
    path('orders/user/', UserOrderListView.as_view(), name='user_orders'),
    path('orders/', OrderCreateView.as_view(), name='create_order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/', OrderStatusUpdateView.as_view(), name='update_order_status'),
] 