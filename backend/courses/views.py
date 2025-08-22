from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from .models import Course, Category, Level, SiteContent, Feature, CourseReview
from .serializers import (
    CourseSerializer, CategorySerializer, LevelSerializer,
    SiteContentSerializer, FeatureSerializer, CourseReviewSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [permissions.AllowAny]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().select_related('category', 'level', 'teacher')
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['price', 'rating', 'students_count', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        category = self.request.query_params.get('category')
        level = self.request.query_params.get('level')
        featured = self.request.query_params.get('featured')
        if category:
            queryset = queryset.filter(category_id=category)
        if level:
            queryset = queryset.filter(level_id=level)
        if featured:
            queryset = queryset.filter(featured=True)
        return queryset

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_courses = self.get_queryset().filter(featured=True)
        serializer = self.get_serializer(featured_courses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_review(self, request, pk=None):
        course = self.get_object()
        user = request.user
        
        # Check if user already reviewed this course
        existing_review = CourseReview.objects.filter(course=course, user=user).first()
        
        serializer = CourseReviewSerializer(data=request.data)
        if serializer.is_valid():
            if existing_review:
                # Update existing review
                serializer.update(existing_review, serializer.validated_data)
                return Response(serializer.data)
            else:
                # Create new review
                serializer.save(course=course, user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAuthenticated])
    def delete_review(self, request, pk=None):
        course = self.get_object()
        user = request.user
        
        try:
            review = CourseReview.objects.get(course=course, user=user)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CourseReview.DoesNotExist:
            return Response({'error': 'نظر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

class SiteContentViewSet(viewsets.ModelViewSet):
    queryset = SiteContent.objects.all()
    serializer_class = SiteContentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    @action(detail=False, methods=['get'])
    def hero(self, request):
        hero_content = self.get_queryset().filter(content_type__startswith='hero_')
        serializer = self.get_serializer(hero_content, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def features(self, request):
        features_content = self.get_queryset().filter(content_type__startswith='features_')
        serializer = self.get_serializer(features_content, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def instructor(self, request):
        instructor_content = self.get_queryset().filter(content_type__startswith='instructor_')
        serializer = self.get_serializer(instructor_content, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def newsletter(self, request):
        newsletter_content = self.get_queryset().filter(content_type__startswith='newsletter_')
        serializer = self.get_serializer(newsletter_content, many=True)
        return Response(serializer.data)

class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by('order')

class CourseImageUploadView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        if not image:
            return Response({'error': 'هیچ فایلی ارسال نشده است.'}, status=status.HTTP_400_BAD_REQUEST)
        path = default_storage.save(f"courses/{image.name}", ContentFile(image.read()))
        image_url = request.build_absolute_uri(settings.MEDIA_URL + os.path.basename(path))
        return Response({'url': image_url}, status=status.HTTP_201_CREATED)
