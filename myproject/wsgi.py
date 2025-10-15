import os
import sys

# Project root directory (manage.py যেখানে আছে)
project_home = '/home/yourusername/myapp'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
