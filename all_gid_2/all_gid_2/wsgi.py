"""
WSGI config for all_gid_2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'all_gid_2.settings')


project_folder = os.path.expanduser('~/all_gid_2')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

application = get_wsgi_application()
