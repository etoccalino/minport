from django.db import models
from django.contrib.auth.models import User


class Consumer (User):
    class Meta:
        proxy = True

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Package (models.Model):

    # Who bought the package. NULL if package has not been bought.
    buyer = models.ForeignKey(Consumer, null=True,
                              related_name='packages_bought')


class ItemOrder (models.Model):
    "An intention to buy a number of a particular item."

    # Who ordered this item.
    consumer = models.ForeignKey(Consumer, related_name='item_orders',
                                 editable=False)

    # Descriptive name of the item to buy.
    item_name = models.CharField('nombre del artIculo',
                                 max_length=30, blank=False)

    # Cost of an individual item.
    item_cost = models.DecimalField('costo individual',
                                    decimal_places=2, max_digits=5)

    # Number of items to buy.
    quantity = models.PositiveIntegerField('cantidad a comprar', default=1)

    # How much the consumer is willing to pay for shipping.
    max_shipping_cost = models.DecimalField(
        'quE tanto pensas pagar de shipping?', decimal_places=2, max_digits=5)

    # URL in the provider's domain
    url = models.URLField(blank=True)

    # Whether this item order has been bought.
    #
    # TRUE means the 'package' attribute should be used. FALSE means the item
    # order is still potential, and the 'potential_packages' attribute should
    # be used instead.
    bought = models.BooleanField(default=False, editable=False)
    package = models.ForeignKey(
        Package, related_name='item_orders', null=True, editable=False)
    potential_packages = models.ManyToManyField(
        Package, related_name='potential_item_orders', editable=False)

    def total_cost(self):
        "Total cost of the order (no discounts applied), in cents."
        return self.item.cost * self.quantity
