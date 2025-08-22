from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'rating', 'featured', 'is_active', 'created_at']
    list_filter = ['rating', 'featured', 'is_active', 'created_at']
    search_fields = ['name', 'content']
    list_editable = ['featured', 'is_active', 'rating']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'role', 'content', 'rating')
        }),
        ('تصویر', {
            'fields': ('image',),
            'classes': ('collapse',)
        }),
        ('تنظیمات', {
            'fields': ('featured', 'is_active')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
