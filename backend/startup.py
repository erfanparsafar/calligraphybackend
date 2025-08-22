#!/usr/bin/env python
"""
Startup script for Calligraphy Backend
This script runs during server startup to ensure the admin user exists
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

from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()

def ensure_admin_user():
    """Ensure admin user exists, create if not"""
    try:
        # Check if admin user exists
        if not User.objects.filter(username='admin').exists():
            print("👤 Admin user not found. Creating...")
            call_command('create_admin_user', verbosity=0)
            print("✅ Admin user created successfully!")
        else:
            print("✅ Admin user already exists")
            
        # Print admin credentials
        admin_user = User.objects.get(username='admin')
        print(f"📋 Admin credentials:")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Is Superuser: {admin_user.is_superuser}")
        print(f"   Is Staff: {admin_user.is_staff}")
        
    except Exception as e:
        print(f"❌ Error ensuring admin user: {str(e)}")
        # Don't raise the error during startup

def check_database():
    """Check database connection"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")

def main():
    """Main startup function"""
    print("🚀 Starting Calligraphy Backend...")
    
    try:
        # Check database
        check_database()
        
        # Ensure admin user exists
        ensure_admin_user()
        
        print("🎉 Startup completed successfully!")
        
    except Exception as e:
        print(f"❌ Startup failed: {str(e)}")
        # Don't exit during startup, just log the error

if __name__ == '__main__':
    main()
