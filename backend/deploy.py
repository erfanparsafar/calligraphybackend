#!/usr/bin/env python
"""
Deployment script for Calligraphy Backend
This script runs automatically during deployment to set up the production environment
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

def main():
    """Main deployment function"""
    print("🚀 Starting deployment process...")
    
    try:
        # 1. Run migrations
        print("📊 Running database migrations...")
        call_command('migrate', verbosity=1)
        
        # 2. Collect static files
        print("📁 Collecting static files...")
        call_command('collectstatic', '--noinput', verbosity=1)
        
        # 3. Create admin user
        print("👤 Creating admin user...")
        call_command('create_admin_user', verbosity=1)
        
        # 4. Check database connection
        print("🔍 Checking database connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
        
        print("🎉 Deployment completed successfully!")
        print("\n📋 Admin credentials:")
        print("   Username: admin")
        print("   Password: admin")
        print("   Email: admin@calligraphy.com")
        print("\n🔗 Admin panel: /admin/")
        
    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
