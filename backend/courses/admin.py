from django.contrib import admin
from .models import Course, Category, Level, SiteContent, Feature, CourseContent, CourseSection, CourseLesson, CourseReview

class CourseLessonInline(admin.TabularInline):
    model = CourseLesson
    extra = 1
    ordering = ['order']

class CourseSectionInline(admin.TabularInline):
    model = CourseSection
    extra = 1
    ordering = ['order']
    inlines = [CourseLessonInline]

class CourseContentInline(admin.StackedInline):
    model = CourseContent
    extra = 0

class CourseReviewInline(admin.TabularInline):
    model = CourseReview
    extra = 0
    readonly_fields = ['created_at']
    can_delete = False

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'level', 'price', 'duration', 'students_count', 'rating', 'featured', 'is_active']
    list_filter = ['category', 'level', 'featured', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['featured', 'is_active']
    inlines = [CourseContentInline, CourseSectionInline, CourseReviewInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'description', 'image', 'price', 'category', 'level', 'duration')
        }),
        ('آمار و امتیازات', {
            'fields': ('students_count', 'rating', 'review_count', 'featured')
        }),
        ('تنظیمات', {
            'fields': ('is_active', 'tags', 'teacher')
        }),
    )

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'title', 'is_active']
    list_filter = ['content_type', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['is_active']

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title']

@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    list_editable = ['order']
    search_fields = ['title', 'course__title']
    inlines = [CourseLessonInline]

@admin.register(CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'duration', 'order']
    list_filter = ['section__course']
    list_editable = ['duration', 'order']
    search_fields = ['title', 'section__title']

@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'course']
    search_fields = ['user__username', 'course__title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
