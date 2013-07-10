from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import FormView

from models import Consumer, ItemOrder, Item, Constrains
from forms import ItemOrderForm


class ItemOrders (ListView):
    template_name = 'base/item_orders.html'
    context_object_name = 'item_orders_list'

    def get_queryset(self):
        return ItemOrder.objects.filter(bought=False,
                                        consumer=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemOrders, self).dispatch(*args, **kwargs)


class NewItemOrder (FormView):
    template_name = 'base/new_item_order.html'
    form_class = ItemOrderForm
    success_url = reverse_lazy('base:home')

    def form_valid(self, form):
        result = super(NewItemOrder, self).form_valid(form)
        data = form.cleaned_data

        # Create the item for the order
        item = Item(name=data['item_name'],
                    cost=data['item_cost'],
                    url=data['url'])
        item.save()
        # Create the order constrains
        constrains = Constrains(max_shipping_cost=data['max_shipping_cost'])
        constrains.save()
        # Create the order and associate it
        consumer = Consumer.objects.get(pk=self.request.user.pk)
        order = ItemOrder(consumer=consumer,
                          quantity=data['quantity'])
        order.item = item
        order.constrains = constrains
        order.save()

        return result
