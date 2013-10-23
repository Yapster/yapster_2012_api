"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize registration behavior, feel free to set up
your own URL patterns for these views instead.

"""


from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.views.generic.base import TemplateView

from registration.backends.default.views_api import ActivationView
from registration.backends.default.views_api import RegistrationView


urlpatterns = patterns('',
                       url(r'^activate/$',
                           ActivationView.as_view(),
                           name='api_registration_activate'),
                       url(r'^register/$',
                           RegistrationView.as_view(),
                           name='api_registration_register'),
                       )
