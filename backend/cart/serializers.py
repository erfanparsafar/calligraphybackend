from rest_framework import serializers
from .models import Cart, CartItem
from courses.serializers import CourseSerializer

class CartItemSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=CourseSerializer.Meta.model.objects.all(), source='course', write_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'course', 'course_id', 'quantity', 'added_at', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at'] 