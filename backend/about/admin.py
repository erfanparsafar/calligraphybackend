from django.contrib import admin
from .models import AboutPage

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    search_fields = ['title', 'content']
    list_filter = ['is_active']
