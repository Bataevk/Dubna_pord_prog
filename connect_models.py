import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# wsgi apllications
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from models.models import *