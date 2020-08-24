import os

from app.settings.components import BASE_DIR

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = False

ALLOWED_HOSTS = [
    os.environ.get('DOMAIN')
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
