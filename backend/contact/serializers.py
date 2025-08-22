from rest_framework import serializers
from .models import ContactInfo, ContactMessage

class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = [
            'id', 'title', 'description',
            'address', 'phone', 'mobile', 'email', 'fax',
            'working_hours',
            'instagram', 'telegram', 'whatsapp', 'linkedin', 'twitter',
            'map_embed', 'latitude', 'longitude',
            'contact_form_title', 'contact_form_description',
            'is_active', 'order',
            'created_at', 'updated_at'
        ]

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'status', 'created_at']
        read_only_fields = ['status', 'created_at'] 