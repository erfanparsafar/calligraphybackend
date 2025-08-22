from django.contrib import admin
from .models import ContactInfo, ContactMessage

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'phone', 'email', 'is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'address', 'phone', 'email']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'description')
        }),
        ('اطلاعات تماس', {
            'fields': ('address', 'phone', 'mobile', 'email', 'fax')
        }),
        ('ساعات کاری', {
            'fields': ('working_hours',),
            'classes': ('collapse',)
        }),
        ('شبکه‌های اجتماعی', {
            'fields': ('instagram', 'telegram', 'whatsapp', 'linkedin', 'twitter'),
            'classes': ('collapse',)
        }),
        ('نقشه و موقعیت', {
            'fields': ('map_embed', 'latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('فرم تماس', {
            'fields': ('contact_form_title', 'contact_form_description'),
            'classes': ('collapse',)
        }),
        ('تنظیمات', {
            'fields': ('is_active', 'order')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'ip_address', 'created_at', 'updated_at']
    list_editable = ['status']
    
    fieldsets = (
        ('اطلاعات فرستنده', {
            'fields': ('name', 'email', 'phone')
        }),
        ('پیام', {
            'fields': ('subject', 'message')
        }),
        ('وضعیت', {
            'fields': ('status',)
        }),
        ('اطلاعات فنی', {
            'fields': ('ip_address', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False  # پیام‌ها فقط از طریق فرم سایت ایجاد می‌شوند
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
