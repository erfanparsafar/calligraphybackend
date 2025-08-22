from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from courses.models import Course
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

# Create your views here.

class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        course_id = request.data.get('course_id')
        quantity = request.data.get('quantity', 1)
        course = get_object_or_404(Course, id=course_id)
        item, created = CartItem.objects.get_or_create(cart=cart, course=course)
        item.quantity = quantity
        item.save()
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        return Response({'detail': 'Cart cleared.'}, status=status.HTTP_204_NO_CONTENT)

class UpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, item_id):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        quantity = request.data.get('quantity', 1)
        item.quantity = quantity
        item.save()
        serializer = CartItemSerializer(item)
        return Response(serializer.data)

class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id):
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return Response({'detail': 'Item removed from cart.'}, status=status.HTTP_204_NO_CONTENT)
