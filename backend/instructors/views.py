from rest_framework import viewsets, permissions
from .models import InstructorProfile
from .serializers import InstructorProfileSerializer

class InstructorProfileViewSet(viewsets.ModelViewSet):
    queryset = InstructorProfile.objects.filter(is_active=True)
    serializer_class = InstructorProfileSerializer
    permission_classes = [permissions.AllowAny] 