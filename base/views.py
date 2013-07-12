from django.shortcuts import get_object_or_404, redirect, render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView

from models import Consumer, ItemOrder
from forms import NewItemOrderForm, EditItemOrderForm


class ItemOrders (View):
    def get(self, request):
        return render(request, 'base/item_orders.html', {
            'consumer': Consumer.objects.get(pk=self.request.user.pk)
        })


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


class EditItemOrder (UpdateView):
    template_name = 'base/item_order_form.html'
    model = ItemOrder
    form_class = EditItemOrderForm
    success_url = reverse_lazy('base:home')


class RemoveItemOrder (View):
    def post(self, request, pk):
        item = get_object_or_404(ItemOrder, pk=pk)
        consumer = Consumer.objects.get(pk=self.request.user.pk)
        if item.consumer == consumer:
            item.delete()
        else:
            item.packages.remove(consumer.package)
        return redirect('base:home')
