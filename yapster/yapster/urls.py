from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^api/accounts/', include('registration.backends.default.urls_api')),
    url(r'^api/yap/', include('yap.urls_api')),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
    # Examples:
    # url(r'^$', 'yapster.views.home', name='home'),
    # url(r'^yapster/', include('yapster.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
