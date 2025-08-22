#!/usr/bin/env python
"""
Production deployment script for Calligraphy Backend
This script runs during production deployment to set up the environment
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
from django.db import connection
from django.conf import settings

def production_deploy():
    """Production deployment process"""
    print("🚀 Starting production deployment...")
    
    try:
        # 1. Check if we're in production
        if not settings.DEBUG:
            print("✅ Production environment detected")
        else:
            print("⚠️ Warning: DEBUG is True in production!")
        
        # 2. Run migrations
        print("📊 Running database migrations...")
        call_command('migrate', '--noinput', verbosity=1)
        
        # 3. Collect static files
        print("📁 Collecting static files...")
        call_command('collectstatic', '--noinput', verbosity=1)
        
        # 4. Create admin user if not exists
        print("👤 Ensuring admin user exists...")
        call_command('create_admin_user', verbosity=1)
        
        # 5. Check database connection
        print("🔍 Checking database connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
        
        # 6. Check system health
        print("🏥 Checking system health...")
        call_command('check', '--deploy', verbosity=1)
        
        print("🎉 Production deployment completed successfully!")
        print("\n📋 System Information:")
        print(f"   Django Version: {django.get_version()}")
        print(f"   Database: {settings.DATABASES['default']['ENGINE']}")
        print(f"   Static Root: {settings.STATIC_ROOT}")
        print(f"   Media Root: {settings.MEDIA_ROOT}")
        print("\n🔑 Admin credentials:")
        print("   Username: admin")
        print("   Password: admin")
        print("   Email: admin@calligraphy.com")
        print("\n🔗 Admin panel: /admin/")
        
    except Exception as e:
        print(f"❌ Production deployment failed: {str(e)}")
        raise

def create_superuser():
    """Create a superuser interactively"""
    print("👤 Creating superuser interactively...")
    call_command('createsuperuser', interactive=True)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--superuser':
        create_superuser()
    else:
        production_deploy()
