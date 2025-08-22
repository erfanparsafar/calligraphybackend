from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.serializers import UserSerializer
from courses.serializers import CourseSerializer
from orders.serializers import OrderSerializer
from courses.models import Course
from orders.models import Order
from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your views here.

class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user, status='paid')
        enrolled_courses = [item.course for order in orders for item in order.items.all()]
        completed_courses = []  # اگر نیاز به پیاده‌سازی دارید
        total_spent = sum(order.total_price for order in orders)
        orders_count = orders.count()
        data = {
            'user': UserSerializer(user).data,
            'enrolled_courses': CourseSerializer(enrolled_courses, many=True).data,
            'completed_courses': [],
            'total_spent': total_spent,
            'orders_count': orders_count,
        }
        return Response(data)

class UserEnrolledCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user, status='paid')
        enrolled_courses = []
        
        for order in orders:
            for item in order.items.all():
                # Calculate progress based on order date (mock data for now)
                days_since_order = (timezone.now() - order.created_at).days
                progress = min(100, max(10, days_since_order * 5))  # Mock progress
                
                course_data = CourseSerializer(item.course).data
                course_data['progress'] = progress
                course_data['lastAccessed'] = self.get_last_accessed_text(order.created_at)
                course_data['orderDate'] = order.created_at
                
                enrolled_courses.append(course_data)
        
        return Response(enrolled_courses)

    def get_last_accessed_text(self, order_date):
        days_diff = (timezone.now() - order_date).days
        if days_diff == 0:
            return 'امروز'
        elif days_diff == 1:
            return 'دیروز'
        elif days_diff < 7:
            return f'{days_diff} روز پیش'
        elif days_diff < 30:
            weeks = days_diff // 7
            return f'{weeks} هفته پیش'
        else:
            months = days_diff // 30
            return f'{months} ماه پیش'

class UserCertificatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Get completed courses (courses with progress 100%)
        orders = Order.objects.filter(user=user, status='paid')
        completed_courses = []
        
        for order in orders:
            for item in order.items.all():
                # Mock: consider courses older than 30 days as completed
                days_since_order = (timezone.now() - order.created_at).days
                if days_since_order > 30:
                    certificate_data = {
                        'id': f"cert_{item.course.id}_{order.id}",
                        'title': f'گواهی دوره {item.course.title}',
                        'date': order.created_at.strftime('%Y/%m/%d'),
                        'downloadUrl': f'/api/certificates/{item.course.id}/download/',
                        'courseId': item.course.id,
                        'courseTitle': item.course.title
                    }
                    completed_courses.append(certificate_data)
        
        return Response(completed_courses)

class UserFavoritesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # For now, return recently viewed courses as favorites
        # In a real app, you'd have a separate Favorites model
        recent_orders = Order.objects.filter(user=user, status='paid').order_by('-created_at')[:5]
        favorites = []
        
        for order in recent_orders:
            for item in order.items.all():
                course_data = CourseSerializer(item.course).data
                course_data['isFavorite'] = True
                favorites.append(course_data)
        
        # Add some popular courses as favorites if user has few
        if len(favorites) < 3:
            popular_courses = Course.objects.filter(is_active=True).order_by('-students_count')[:3]
            for course in popular_courses:
                if not any(fav['id'] == course.id for fav in favorites):
                    course_data = CourseSerializer(course).data
                    course_data['isFavorite'] = True
                    favorites.append(course_data)
        
        return Response(favorites[:6])  # Return max 6 favorites

class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_users = UserSerializer.Meta.model.objects.count()
        total_courses = Course.objects.count()
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(status='paid').aggregate(models.Sum('total_price'))['total_price__sum'] or 0
        recent_orders = Order.objects.order_by('-created_at')[:5]
        top_courses = Course.objects.order_by('-students_count')[:5]
        data = {
            'total_users': total_users,
            'total_courses': total_courses,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'recent_orders': OrderSerializer(recent_orders, many=True).data,
            'top_courses': CourseSerializer(top_courses, many=True).data,
        }
        return Response(data)
