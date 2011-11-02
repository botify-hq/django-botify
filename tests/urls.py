from django.conf.urls.defaults import *

from tests.views import simple, tracker, canonical

urlpatterns = patterns(
    '',
    url(r'simple/',
        simple,
        name='simple'),
    url(r'canonical/',
        canonical,
        name='canonical'),
    url(r'tracker/',
        tracker,
        name='tracker')
)
