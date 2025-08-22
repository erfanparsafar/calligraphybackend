from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

# Create your views here.

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all().select_related('user')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price,
            status='pending',
            payment_method=request.data.get('payment_method', 'online'),
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                course=item.course,
                quantity=item.quantity,
                price=item.course.price,
            )
        cart.items.all().delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderStatusUpdateView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        status_value = request.data.get('status')
        if status_value:
            order.status = status_value
            order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
