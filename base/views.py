from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class Home (TemplateView):
    template_name = 'base/home.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Home, self).dispatch(*args, **kwargs)
