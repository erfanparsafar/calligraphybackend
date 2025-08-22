from rest_framework import serializers
from .models import Course, Category, Level, SiteContent, Feature, CourseContent, CourseSection, CourseLesson, CourseReview
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class CourseLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ['id', 'title', 'description', 'duration', 'video_url', 'order']

class CourseSectionSerializer(serializers.ModelSerializer):
    lessons = CourseLessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = CourseSection
        fields = ['id', 'title', 'description', 'order', 'lessons']

class CourseContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseContent
        fields = ['introduction', 'prerequisites', 'what_you_learn']

class CourseReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = CourseReview
        fields = ['id', 'rating', 'comment', 'created_at', 'user_name', 'user_username']
        read_only_fields = ['user', 'created_at']

class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    level = LevelSerializer(read_only=True)
    level_name = serializers.CharField(source='level.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    content = CourseContentSerializer(read_only=True)
    sections = CourseSectionSerializer(many=True, read_only=True)
    reviews = CourseReviewSerializer(many=True, read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    level_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    teacher_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    image = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'image', 'price', 
            'category', 'category_name', 'level', 'level_name',
            'duration', 'students_count', 'rating', 'review_count', 
            'featured', 'is_active', 'tags',
            'teacher', 'teacher_name', 'created_at', 'updated_at',
            'content', 'sections', 'reviews', 'category_id', 'level_id', 'teacher_id'
        ]
        read_only_fields = ['id', 'last_update', 'created_at', 'updated_at', 'content', 'sections', 'reviews', 'category_name', 'level_name', 'teacher_name', 'category', 'level', 'teacher', 'students_count', 'rating', 'review_count']

class SiteContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteContent
        fields = [
            'id', 'content_type', 'title', 'subtitle', 'description',
            'button_text', 'button_url', 'image', 'is_active',
            'created_at', 'updated_at'
        ]

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = [
            'id', 'title', 'description', 'icon', 'order',
            'is_active', 'created_at', 'updated_at'
        ] 