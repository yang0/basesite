# SECURITY WARNING: don't run with debug turned on in production!
# import pymysql
# pymysql.install_as_MySQLdb()

import os

DEBUG = True

# DOMAIN = 'https://test.beex1.cn'
DOMAIN = 'https://127.0.0.1'
DB_HOST = '127.0.0.1'

ALLOWED_HOSTS = (
    ['localhost', '127.0.0.1', ] +
    ['192.168.2.%d' % i for i in range(256)] +
    ['192.168.1.%d' % i for i in range(256)])

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'apps.common.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': 'abc123',
        'HOST': DB_HOST,
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        },
    }
}

# RUN_ENV
RUN_ENV = 'dev'

