from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'base.views.home', name='home'),
)
