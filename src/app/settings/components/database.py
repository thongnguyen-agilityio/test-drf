import os

from app.settings.components import BASE_DIR

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'NAME': os.environ.get('DATABASE_NAME', 'membership_management'),
        'USER': os.environ.get('DATABASE_USER', 'membership_management'),
        'ENGINE': 'django.db.backends.postgresql',
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'membership_management'),
        'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DATABASE_PORT', 5432),
    }
}
