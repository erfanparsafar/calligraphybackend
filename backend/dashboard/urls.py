from django.urls import path
from .views import UserDashboardView, AdminDashboardView, UserEnrolledCoursesView, UserCertificatesView, UserFavoritesView

urlpatterns = [
    path('user/', UserDashboardView.as_view(), name='user-dashboard'),
    path('admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('user/enrolled-courses/', UserEnrolledCoursesView.as_view(), name='user-enrolled-courses'),
    path('user/certificates/', UserCertificatesView.as_view(), name='user-certificates'),
    path('user/favorites/', UserFavoritesView.as_view(), name='user-favorites'),
] 