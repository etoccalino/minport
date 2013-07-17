import json
from django.http import HttpResponse
from django.views.generic.base import View
from autocomplete import Complete


class SimpleCompleter (View):
    def get(self, request):
        article_url = request.GET.get('q')
        if not article_url:
            # No "q" is an automatic client error.
            return HttpResponse(status=400)
        try:
            completer = Complete(url=article_url)
            return HttpResponse(content_type="application/json",
                                content=json.dumps({
                                    "name": completer.name(),
                                    "price": completer.price(),
                                }))
        except ValueError:
            return HttpResponse(status=400)
        except LookupError:
            return HttpResponse(status=500)
