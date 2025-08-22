#!/usr/bin/env python
"""
Debug script for dashboard endpoints
This script helps identify issues with dashboard API endpoints
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
import json

def test_dashboard_endpoints():
    """Test all dashboard endpoints"""
    client = Client()
    
    print("🔍 Testing Dashboard Endpoints...")
    print("=" * 50)
    
    # Test 1: Test endpoint without authentication
    print("\n1️⃣ Testing /api/dashboard/test/ (no auth required)")
    try:
        response = client.get('/api/dashboard/test/')
        print(f"   Status: {response.status_code}")
        print(f"   Content: {response.content.decode()[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Test admin endpoint without authentication
    print("\n2️⃣ Testing /api/dashboard/admin/ (no auth)")
    try:
        response = client.get('/api/dashboard/admin/')
        print(f"   Status: {response.status_code}")
        print(f"   Content: {response.content.decode()[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Create a test user and authenticate
    print("\n3️⃣ Creating test user...")
    try:
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            print(f"   Created user: {test_user.username}")
        else:
            print(f"   User exists: {test_user.username}")
    except Exception as e:
        print(f"   Error creating user: {e}")
        return
    
    # Test 4: Test admin endpoint with authentication
    print("\n4️⃣ Testing /api/dashboard/admin/ (with auth)")
    try:
        client.login(username='testuser', password='testpass123')
        response = client.get('/api/dashboard/admin/')
        print(f"   Status: {response.status_code}")
        print(f"   Content: {response.content.decode()[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Test user dashboard endpoint
    print("\n5️⃣ Testing /api/dashboard/user/ (with auth)")
    try:
        response = client.get('/api/dashboard/user/')
        print(f"   Status: {response.status_code}")
        print(f"   Content: {response.content.decode()[:200]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 6: Check URL patterns
    print("\n6️⃣ Checking URL patterns...")
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        url_patterns = []
        
        def collect_urls(patterns, prefix=''):
            for pattern in patterns:
                if hasattr(pattern, 'url_patterns'):
                    collect_urls(pattern.url_patterns, prefix + str(pattern.pattern))
                else:
                    url_patterns.append(prefix + str(pattern.pattern))
        
        collect_urls(resolver.url_patterns)
        
        dashboard_urls = [url for url in url_patterns if 'dashboard' in url]
        print(f"   Dashboard URLs found: {dashboard_urls}")
        
    except Exception as e:
        print(f"   Error checking URLs: {e}")
    
    # Test 7: Check if models exist
    print("\n7️⃣ Checking models...")
    try:
        from users.models import User as CustomUser
        from courses.models import Course
        from orders.models import Order
        
        print(f"   User model: {CustomUser}")
        print(f"   Course model: {Course}")
        print(f"   Order model: {Order}")
        
        # Check if tables exist
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"   Available tables: {tables}")
            
    except Exception as e:
        print(f"   Error checking models: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Dashboard endpoint testing completed!")

if __name__ == '__main__':
    test_dashboard_endpoints()
