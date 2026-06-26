import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Base Directories and Environment Setup
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the root .env file securely
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 2. Security Configurations
# In production, this will read from your environment instead of hardcoded strings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-local-key-change-this-in-prod')

# Safety switch: Automatically defaults to False if not explicitly set to True in .env
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Allow local system execution and cloud platform host configurations
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.onrender.com', '.pythonanywhere.com']


# 3. Application Definitions
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookings', # Your local multi-service booking application
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# 4. Database Schema Engine
# Production-ready persistent SQLite file storage
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# 5. Internationalization & Regional Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata' # Locked to Indian Standard Time (IST) for regional inquiries
USE_I18N = True
USE_TZ = True


# 6. Static Asset Handling Engine (Production and Local Development Layouts)
STATIC_URL = 'static/'

# Local directories where Django searches for asset sources during workspace execution
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'bookings/static'),
]

# The production deployment destination folder where 'collectstatic' bundles assets for fast web hosting
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# 7. Default Primary Key Field Type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'