"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Import and run startup script
try:
    from startup import main as startup_main
    startup_main()
except ImportError:
    # If startup script is not available, continue without it
    pass
except Exception as e:
    # Log startup errors but don't fail the WSGI application
    print(f"Startup script error (non-critical): {e}")

application = get_wsgi_application()
