import os
from app.settings.components.common import (
    INSTALLED_APPS,
    MIDDLEWARE,
)
from app.settings.components import BASE_DIR

# development settings

DEBUG = False

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'NAME': os.environ.get('DATABASE_NAME', 'drf'),
        'USER': os.environ.get('DATABASE_USER', 'basedrf'),
        'ENGINE': 'django.db.backends.postgresql',
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'basedrf1234'),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', 5432),
    }
}

# No need whitelist, all origins will be accepted
CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = [
    os.environ.get('DOMAIN'),
    'localhost',
    '127.0.0.1',
]

import requests

EC2_PRIVATE_IP = None
METADATA_URI = os.environ.get('ECS_CONTAINER_METADATA_URI')

try:
    resp = requests.get(METADATA_URI)
    data = resp.json()
    print(data)

    EC2_PRIVATE_IP = data['Networks'][0]['IPv4Addresses'][0]
except:
    # silently fail as we may not be in an ECS environment
    pass

if EC2_PRIVATE_IP:
    # Be sure your ALLOWED_HOSTS is a list NOT a tuple
    # or .append() will fail
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

print('EC2_PRIVATE_IP', EC2_PRIVATE_IP)
