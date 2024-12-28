from pathlib import Path
import os 


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-zyv@=-fp*7uxnwwb(e=+gxqj+965*2s(yj*k9dau!ull6%-um='

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'channels',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SrcApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'chat_application.urls'

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

ASGI_APPLICATION = 'chat_application.asgi.application'


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CSP_SCRIPT_SRC = (
    "'self'",
    "https://kit.fontawesome.com",  # Correct domain for Font Awesome scripts
    "'unsafe-inline'",             # If inline scripts are used
    "'unsafe-eval'",               # If eval() is needed (usually discouraged)
)

CSP_DEFAULT_SRC = ("'self'",)

CSP_CONNECT_SRC = (
    "'self'", 
    "ws://127.0.0.1:8000",  
    "https://ka-f.fontawesome.com"  # Allow Font Awesome connections
)

CSP_IMG_SRC = ("'self'", "data:")

CSP_STYLE_SRC = (
    "'self'",
    "https://kit.fontawesome.com", # Allow Font Awesome styles
    "'unsafe-inline'",            # Allow inline styles if needed
)

CSP_FONT_SRC = (
    "'self'",
    "https://kit.fontawesome.com",
    "https://ka-f.fontawesome.com",  # Allow Font Awesome webfonts
    "https://cdnjs.cloudflare.com",  # Optional if used
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root_folder')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
