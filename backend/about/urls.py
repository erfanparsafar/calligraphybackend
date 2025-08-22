from django.urls import path
from .views import (
    AboutPageListView,
    AboutPageDetailView,
    AboutPageAdminView,
    AboutPageAdminDetailView
)

urlpatterns = [
    # Public endpoints
    path('', AboutPageListView.as_view(), name='about_list'),
    path('<int:pk>/', AboutPageDetailView.as_view(), name='about_detail'),
    
    # Admin endpoints
    path('admin/', AboutPageAdminView.as_view(), name='about_admin_list'),
    path('admin/<int:pk>/', AboutPageAdminDetailView.as_view(), name='about_admin_detail'),
] 