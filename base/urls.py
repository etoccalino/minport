from django.conf.urls import patterns, url
from views import EditItemOrder, NewItemOrder, ItemOrders


urlpatterns = patterns('',
    url(r'^nuevo/$', NewItemOrder.as_view(), name='new_item_order'),
    url(r'^editar/(?P<pk>\d+)/$', EditItemOrder.as_view(), name='edit_item_order'),
    url(r'^$', ItemOrders.as_view(), name='home'),
)
