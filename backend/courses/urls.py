from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, CategoryViewSet, LevelViewSet, SiteContentViewSet, FeatureViewSet, CourseImageUploadView
from django.urls import path

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'site-content', SiteContentViewSet, basename='site-content')
router.register(r'features', FeatureViewSet, basename='feature')

urlpatterns = router.urls + [
    path('upload-course-image/', CourseImageUploadView.as_view(), name='course-upload-image'),
] 