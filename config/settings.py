"""
Django settings for SmartPilgrim (config project).
Finalized for B.Tech 4th Year Project Scope.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j^$u@(mj8f95y^yk9hz!$tccpz+sm=8p)p!hg#06%%%0n2da7b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition - Updated to match project dir
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Internal Project Apps 
    'accounts',      # Auth & Profile
    'temples',       # Registry & Maps
    'bookings',      # Slots & QR
    'crowd_ai',      # Prediction Logic
    'contributions', # Dakshan
    'safety',        # SOS & Alerts
    'management',    # Admin Dashboard
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database - Low-Moderate Complexity standard [cite: 156, 365]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static and Media Files [cite: 345, 158]
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model (Must exist in accounts/models.py) [cite: 50, 222]
AUTH_USER_MODEL = 'accounts.User'

# --- PROJECT SPECIFIC SETTINGS ---

# Frozen UI Theme: "Divine Clarity" (Light Theme Only) [cite: 237, 464]
# Aligned to project title "SmartPilgrim"
THEME_PRIMARY = "#1A5F7A"   # Deep Teal Blue (Nav/Headers)
THEME_ACCENT = "#FFC107"    # Amber Gold (Glowing Buttons) [cite: 343]
THEME_BG_LIGHT = "#F8F9FA"  # Ghost White (Section Backgrounds)
THEME_TEXT = "#2D3436"      # Dark Slate (Typography)

# ---------------- EMAIL CONFIGURATION ---------------- #

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = 'harisaiparasa@gmail.com'
EMAIL_HOST_PASSWORD = 'zdiumjywpwxcvdbd'  # No spaces

DEFAULT_FROM_EMAIL = 'SmartPilgrim Support <harisaiparasa@gmail.com>'

EMAIL_TIMEOUT = 15


# Authentication Redirects
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'