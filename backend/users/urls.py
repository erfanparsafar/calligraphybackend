from django.urls import path
from .views import (
    RegisterView, 
    CustomTokenObtainPairView, 
    CurrentUserView,
    UserListView,
    UserDetailView,
    CreateUserView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('list/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('create/', CreateUserView.as_view(), name='create_user'),
] 