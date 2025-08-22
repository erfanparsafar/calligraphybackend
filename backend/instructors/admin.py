from django.contrib import admin
from .models import InstructorProfile

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'experience_years', 'students_count', 'courses_count', 'featured', 'is_active', 'order']
    list_filter = ['is_active', 'featured', 'created_at']
    search_fields = ['name', 'bio', 'email']
    list_editable = ['featured', 'is_active', 'order']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'title', 'bio', 'short_bio')
        }),
        ('تصاویر', {
            'fields': ('profile_image', 'cover_image'),
            'classes': ('collapse',)
        }),
        ('اطلاعات تماس', {
            'fields': ('email', 'phone', 'website'),
            'classes': ('collapse',)
        }),
        ('شبکه‌های اجتماعی', {
            'fields': ('instagram', 'telegram', 'linkedin'),
            'classes': ('collapse',)
        }),
        ('آمار و اطلاعات', {
            'fields': ('experience_years', 'students_count', 'courses_count')
        }),
        ('مهارت‌ها و تخصص‌ها', {
            'fields': ('skills', 'specializations'),
            'classes': ('collapse',)
        }),
        ('گواهینامه‌ها و افتخارات', {
            'fields': ('certificates', 'awards'),
            'classes': ('collapse',)
        }),
        ('تنظیمات', {
            'fields': ('is_active', 'featured', 'order')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order', '-created_at') 