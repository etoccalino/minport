from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from models import Consumer, ItemOrder
from forms import NewItemOrderForm, EditItemOrderForm


class ItemOrders (ListView):
    template_name = 'base/item_orders.html'
    context_object_name = 'item_orders_list'

    def get_queryset(self):
        consumer = Consumer.objects.get(pk=self.request.user.pk)
        return consumer.package.item_orders.all()

    def get_context_data(self, **kwargs):
        context = super(ItemOrders, self).get_context_data(**kwargs)
        consumer = Consumer.objects.get(pk=self.request.user.pk)
        context['consumer'] = consumer
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemOrders, self).dispatch(*args, **kwargs)


class NewItemOrder (CreateView):
    template_name = 'base/item_order_form.html'
    form_class = NewItemOrderForm
    success_url = reverse_lazy('base:home')

    def form_valid(self, form):
        # Add this consumer to the new item order
        consumer = Consumer.objects.get(pk=self.request.user.pk)
        form.instance.consumer = consumer
        result = super(NewItemOrder, self).form_valid(form)
        # Add this item to all non-bought packages, including this consumer's
        for consumer in Consumer.objects.all():
            consumer.package.item_orders.add(form.instance)
        return result

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewItemOrder, self).dispatch(*args, **kwargs)


class EditItemOrder (UpdateView):
    template_name = 'base/item_order_form.html'
    model = ItemOrder
    form_class = EditItemOrderForm
    success_url = reverse_lazy('base:home')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EditItemOrder, self).dispatch(*args, **kwargs)


class RemoveItemOrder (View):

    def post(self, request, pk):
        item = get_object_or_404(ItemOrder, pk=pk)
        consumer = Consumer.objects.get(pk=self.request.user.pk)
        if item.consumer == consumer:
            item.delete()
        else:
            item.packages.remove(consumer.package)
        return redirect('base:home')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RemoveItemOrder, self).dispatch(*args, **kwargs)
