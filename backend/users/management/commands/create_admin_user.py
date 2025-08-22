from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a default admin user for production deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Admin username (default: admin)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin',
            help='Admin password (default: admin)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@calligraphy.com',
            help='Admin email (default: admin@calligraphy.com)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force creation even if user exists'
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        force = options['force']

        # Check if we're in production environment
        if os.environ.get('DJANGO_SETTINGS_MODULE') != 'core.settings':
            self.stdout.write(
                self.style.WARNING(
                    'This command is designed for production deployment. '
                    'Current environment may not be production.'
                )
            )

        try:
            with transaction.atomic():
                # Check if user already exists
                if User.objects.filter(username=username).exists():
                    if not force:
                        self.stdout.write(
                            self.style.WARNING(
                                f'User "{username}" already exists. Use --force to recreate.'
                            )
                        )
                        return
                    else:
                        # Delete existing user
                        User.objects.filter(username=username).delete()
                        self.stdout.write(
                            self.style.WARNING(f'Deleted existing user "{username}"')
                        )

                # Create new admin user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name='مدیر',
                    last_name='سیستم',
                    is_staff=True,
                    is_superuser=True,
                    is_active=True
                )

                # Give all permissions
                content_types = ContentType.objects.all()
                permissions = Permission.objects.filter(content_type__in=content_types)
                user.user_permissions.set(permissions)

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created admin user "{username}" with full permissions!'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Username: {username}'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Password: {password}'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Email: {email}'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        'You can now login to Django admin panel with these credentials.'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {str(e)}')
            )
            raise
