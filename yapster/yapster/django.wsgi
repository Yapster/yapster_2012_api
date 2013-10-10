import os
import sys
import django.core.handlers.wsgi
sys.path.append('/var/www/yapsterapp.com/yapster')
sys.path.append('/var/www/yapsterapp.com/yapster/yapster')
os.environ['DJANGO_SETTINGS_MODULE'] = 'yapster.settings'
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    return _application(environ, start_response)
