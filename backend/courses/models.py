from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, related_name='courses')
    duration = models.PositiveIntegerField(help_text='تعداد جلسات', blank=True, null=True)
    students_count = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_update = models.DateField(auto_now=True)
    tags = models.JSONField(default=list, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class SiteContent(models.Model):
    CONTENT_TYPES = [
        ('hero_title', 'عنوان اصلی'),
        ('hero_subtitle', 'زیرعنوان اصلی'),
        ('hero_description', 'توضیحات اصلی'),
        ('hero_button_text', 'متن دکمه اصلی'),
        ('hero_button_url', 'لینک دکمه اصلی'),
        ('features_title', 'عنوان ویژگی‌ها'),
        ('features_subtitle', 'زیرعنوان ویژگی‌ها'),
        ('instructor_title', 'عنوان بخش استاد'),
        ('instructor_subtitle', 'زیرعنوان بخش استاد'),
        ('instructor_description', 'توضیحات استاد'),
        ('newsletter_title', 'عنوان خبرنامه'),
        ('newsletter_subtitle', 'زیرعنوان خبرنامه'),
    ]
    
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES, unique=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True, null=True)
    button_url = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='site_content/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_content_type_display()} - {self.title}"

class Feature(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text='نام آیکون Lucide')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class CourseContent(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='content')
    introduction = models.TextField(help_text='معرفی دوره')
    prerequisites = models.TextField(help_text='پیش‌نیازهای دوره')
    what_you_learn = models.TextField(help_text='چه چیزی یاد خواهید گرفت')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"محتوای دوره: {self.course.title}"

class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class CourseLesson(models.Model):
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text='مدت زمان به دقیقه')
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.section.title} - {self.title}"

class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], help_text='امتیاز از 1 تا 5')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['course', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.rating} ستاره"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update course rating and review count
        self.update_course_stats()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # Update course rating and review count
        self.update_course_stats()

    def update_course_stats(self):
        reviews = CourseReview.objects.filter(course=self.course)
        if reviews.exists():
            avg_rating = reviews.aggregate(avg=models.Avg('rating'))['avg']
            review_count = reviews.count()
        else:
            avg_rating = 0
            review_count = 0
        
        self.course.rating = round(avg_rating, 1)
        self.course.review_count = review_count
        self.course.save()
