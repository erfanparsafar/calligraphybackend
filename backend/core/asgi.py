"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Import and run startup script
try:
    from startup import main as startup_main
    startup_main()
except ImportError:
    # If startup script is not available, continue without it
    pass
except Exception as e:
    # Log startup errors but don't fail the ASGI application
    print(f"Startup script error (non-critical): {e}")

application = get_asgi_application()
