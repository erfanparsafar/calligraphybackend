from django.db import models

# Create your models here.

class ContactInfo(models.Model):
    # اطلاعات اصلی
    title = models.CharField(max_length=200, verbose_name="عنوان صفحه تماس")
    description = models.TextField(verbose_name="توضیحات صفحه تماس")
    
    # اطلاعات تماس
    address = models.CharField(max_length=255, verbose_name="آدرس")
    phone = models.CharField(max_length=50, verbose_name="شماره تماس")
    mobile = models.CharField(max_length=50, blank=True, null=True, verbose_name="شماره موبایل")
    email = models.EmailField(verbose_name="ایمیل")
    fax = models.CharField(max_length=50, blank=True, null=True, verbose_name="فکس")
    
    # ساعات کاری
    working_hours = models.TextField(blank=True, null=True, verbose_name="ساعات کاری")
    
    # شبکه‌های اجتماعی
    instagram = models.URLField(blank=True, null=True, verbose_name="اینستاگرام")
    telegram = models.URLField(blank=True, null=True, verbose_name="تلگرام")
    whatsapp = models.URLField(blank=True, null=True, verbose_name="واتساپ")
    linkedin = models.URLField(blank=True, null=True, verbose_name="لینکدین")
    twitter = models.URLField(blank=True, null=True, verbose_name="توییتر")
    
    # نقشه و موقعیت
    map_embed = models.TextField(blank=True, null=True, verbose_name="کد iframe نقشه گوگل")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="عرض جغرافیایی")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="طول جغرافیایی")
    
    # فرم تماس
    contact_form_title = models.CharField(max_length=200, default="فرم تماس با ما", verbose_name="عنوان فرم تماس")
    contact_form_description = models.TextField(blank=True, null=True, verbose_name="توضیحات فرم تماس")
    
    # تنظیمات
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    
    # تاریخ‌ها
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "اطلاعات تماس"
        verbose_name_plural = "اطلاعات تماس"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title or self.address

class ContactMessage(models.Model):
    """مدل برای ذخیره پیام‌های ارسالی از فرم تماس"""
    STATUS_CHOICES = [
        ('new', 'جدید'),
        ('read', 'خوانده شده'),
        ('replied', 'پاسخ داده شده'),
        ('closed', 'بسته'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره تماس")
    subject = models.CharField(max_length=200, verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new', verbose_name="وضعیت")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="آدرس IP")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
