from rest_framework import serializers
from .models import Order, OrderItem
from courses.serializers import CourseSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=CourseSerializer.Meta.model.objects.all(), source='course', write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'course', 'course_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'status', 'payment_method', 'created_at', 'updated_at'] 