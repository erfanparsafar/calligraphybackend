from rest_framework.routers import DefaultRouter
from .views import InstructorProfileViewSet

router = DefaultRouter()
router.register(r'instructors', InstructorProfileViewSet)

urlpatterns = router.urls 