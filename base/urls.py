from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from views import EditItemOrder, NewItemOrder, ItemOrders, RemoveItemOrder


urlpatterns = patterns('',
    url(r'^nuevo/$', login_required(NewItemOrder.as_view()), name='new_item_order'),
    url(r'^editar/(?P<pk>\d+)/$', login_required(EditItemOrder.as_view()), name='edit_item_order'),
    url(r'^remover/(?P<pk>\d+)/$', login_required(RemoveItemOrder.as_view()), name='remove_item_order'),
    url(r'^$', login_required(ItemOrders.as_view()), name='home'),
)
