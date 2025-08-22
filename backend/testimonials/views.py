from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Testimonial
from .serializers import TestimonialSerializer

# Create your views here.

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        featured = self.request.query_params.get('featured')
        if featured:
            queryset = queryset.filter(featured=True)
        return queryset
