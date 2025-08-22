from rest_framework import serializers
from .models import InstructorProfile

class InstructorProfileSerializer(serializers.ModelSerializer):
    skills_list = serializers.SerializerMethodField()
    specializations_list = serializers.SerializerMethodField()
    
    class Meta:
        model = InstructorProfile
        fields = [
            'id', 'name', 'title', 'bio', 'short_bio',
            'profile_image', 'cover_image',
            'email', 'phone', 'website',
            'instagram', 'telegram', 'linkedin',
            'experience_years', 'students_count', 'courses_count',
            'skills', 'skills_list', 'specializations', 'specializations_list',
            'certificates', 'awards',
            'featured', 'order',
            'created_at', 'updated_at'
        ]
    
    def get_skills_list(self, obj):
        return obj.get_skills_list()
    
    def get_specializations_list(self, obj):
        return obj.get_specializations_list() 