from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'cssmanager.views',
    url(r'^dirscss/$', 'dirscss', name='dirscss'),
    url(r'^submitcss/$', 'submitcss', name='submitcss'),
    )
