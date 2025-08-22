#!/bin/bash

# Deployment script for Calligraphy Backend
# This script runs during deployment to set up the production environment

set -e  # Exit on any error

echo "🚀 Starting deployment process..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the backend directory."
    exit 1
fi

# Set environment variables for production
export DJANGO_SETTINGS_MODULE=core.settings
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "📊 Running database makemigrations..."
python manage.py makemigrations --noinput

echo "📊 Running database migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "👤 Creating admin user..."
python manage.py create_admin_user

echo "🔍 Checking database connection..."
python manage.py check --deploy

echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Admin credentials:"
echo "   Username: admin"
echo "   Password: admin"
echo "   Email: admin@calligraphy.com"
echo ""
echo "🔗 Admin panel: /admin/"
echo ""
echo "🚀 Starting Gunicorn server..."
