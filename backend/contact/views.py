from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ContactInfo, ContactMessage
from .serializers import ContactInfoSerializer, ContactMessageSerializer

# Create your views here.

class ContactInfoViewSet(viewsets.ModelViewSet):
    queryset = ContactInfo.objects.filter(is_active=True)
    serializer_class = ContactInfoSerializer
    permission_classes = [permissions.AllowAny]

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # اضافه کردن IP آدرس
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            serializer.save(ip_address=ip)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
