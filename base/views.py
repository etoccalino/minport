from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from models import Consumer, ItemOrder
from forms import NewItemOrderForm, EditItemOrderForm


class ItemOrders (ListView):
    template_name = 'base/item_orders.html'
    context_object_name = 'item_orders_list'

    def get_queryset(self):
        return ItemOrder.objects.filter(bought=False,
                                        consumer=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemOrders, self).dispatch(*args, **kwargs)


class NewItemOrder (CreateView):
    template_name = 'base/item_order_form.html'
    form_class = NewItemOrderForm
    success_url = reverse_lazy('base:home')

    def form_valid(self, form):
        consumer = Consumer.objects.get(pk=self.request.user.pk)
        form.instance.consumer = consumer
        return super(NewItemOrder, self).form_valid(form)


class EditItemOrder (UpdateView):
    template_name = 'base/item_order_form.html'
    model = ItemOrder
    form_class = EditItemOrderForm
    success_url = reverse_lazy('base:home')
