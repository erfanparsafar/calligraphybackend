from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import AboutPage
from .serializers import AboutPageSerializer

# Create your views here.

class AboutPageViewSet(viewsets.ModelViewSet):
    queryset = AboutPage.objects.filter(is_active=True)
    serializer_class = AboutPageSerializer
    permission_classes = [permissions.AllowAny]

class AboutPageListView(generics.ListCreateAPIView):
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return AboutPage.objects.filter(is_active=True)

class AboutPageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class AboutPageAdminView(generics.ListCreateAPIView):
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

class AboutPageAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AboutPage.objects.all()
    serializer_class = AboutPageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
