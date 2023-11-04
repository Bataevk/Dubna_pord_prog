# initialize.py
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()

from django.core.management import call_command
call_command('makemigrations')
call_command('migrate')