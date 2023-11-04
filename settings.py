# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase.db',
    }
}

INSTALLED_APPS = (
    'models',
    )

SECRET_KEY = '6509438376:AAGSd-5pyyVl2PTbCOhlDn7KW-R6j2Dhwh0'
