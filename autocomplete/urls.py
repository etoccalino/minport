from django.conf.urls import patterns, url
from views import SimpleCompleter


urlpatterns = patterns('autocomplete.views',
                       url(r'^$', SimpleCompleter.as_view(), name="simple"),
)
