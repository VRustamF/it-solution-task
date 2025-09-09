from .base_settings import *
import os
from pathlib import Path


from dotenv import load_dotenv
load_dotenv()

# Безопасность
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

STATICFILES_DIRS = [BASE_DIR / "static"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler',}},
    'root': {'handlers': ['console'], 'level': 'DEBUG',},
}
