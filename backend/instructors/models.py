from django.db import models

class InstructorProfile(models.Model):
    # اطلاعات اصلی
    name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="عنوان شغلی")
    bio = models.TextField(blank=True, null=True, verbose_name="بیوگرافی")
    short_bio = models.TextField(max_length=500, blank=True, null=True, verbose_name="بیوگرافی کوتاه")
    
    # تصاویر
    profile_image = models.ImageField(upload_to='instructors/', blank=True, null=True, verbose_name="تصویر پروفایل")
    cover_image = models.ImageField(upload_to='instructors/', blank=True, null=True, verbose_name="تصویر کاور")
    
    # اطلاعات تماس
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره تماس")
    website = models.URLField(blank=True, null=True, verbose_name="وب‌سایت")
    
    # شبکه‌های اجتماعی
    instagram = models.URLField(blank=True, null=True, verbose_name="اینستاگرام")
    telegram = models.URLField(blank=True, null=True, verbose_name="تلگرام")
    linkedin = models.URLField(blank=True, null=True, verbose_name="لینکدین")
    
    # آمار و اطلاعات
    experience_years = models.PositiveIntegerField(default=0, verbose_name="سال‌های تجربه")
    students_count = models.PositiveIntegerField(default=0, verbose_name="تعداد دانشجویان")
    courses_count = models.PositiveIntegerField(default=0, verbose_name="تعداد دوره‌ها")
    
    # مهارت‌ها و تخصص‌ها
    skills = models.TextField(blank=True, null=True, verbose_name="مهارت‌ها (هر مهارت در یک خط)")
    specializations = models.TextField(blank=True, null=True, verbose_name="تخصص‌ها (هر تخصص در یک خط)")
    
    # گواهینامه‌ها و افتخارات
    certificates = models.TextField(blank=True, null=True, verbose_name="گواهینامه‌ها")
    awards = models.TextField(blank=True, null=True, verbose_name="افتخارات و جوایز")
    
    # تنظیمات
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    featured = models.BooleanField(default=False, verbose_name="ویژه")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    
    # تاریخ‌ها
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "پروفایل استاد"
        verbose_name_plural = "پروفایل‌های اساتید"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

    def get_skills_list(self):
        """تبدیل مهارت‌ها به لیست"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split('\n') if skill.strip()]
        return []

    def get_specializations_list(self):
        """تبدیل تخصص‌ها به لیست"""
        if self.specializations:
            return [spec.strip() for spec in self.specializations.split('\n') if spec.strip()]
        return [] 