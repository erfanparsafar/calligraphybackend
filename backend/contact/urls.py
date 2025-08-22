from rest_framework.routers import DefaultRouter
from .views import ContactInfoViewSet, ContactMessageViewSet

router = DefaultRouter()
router.register(r'contact', ContactInfoViewSet, basename='contact')
router.register(r'contact-messages', ContactMessageViewSet, basename='contact-message')

urlpatterns = router.urls 