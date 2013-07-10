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
    consumer = models.ForeignKey(Consumer, related_name='item_orders')

    # Number of items to buy.
    quantity = models.PositiveIntegerField(default=1)

    item = models.OneToOneField('Item')

    # Consumer constrains for this item order.
    constrains = models.OneToOneField('Constrains')

    # Whether this item order has been bought.
    #
    # TRUE means the 'package' attribute should be used. FALSE means the item
    # order is still potential, and the 'potential_packages' attribute should
    # be used instead.
    bought = models.BooleanField(default=False)
    package = models.ForeignKey(Package, related_name='item_orders', null=True)
    potential_packages = models.ManyToManyField(
        Package, related_name='potential_item_orders')

    def total_cost(self):
        "Total cost of the order (no discounts applied), in cents."
        return self.item.cost * self.quantity


class Item (models.Model):
    "An item in the provider that consumers can buy."

    # Descriptive name of the item to buy.
    name = models.CharField(max_length=30, blank=False)

    # Cost of an individual item, in cents.
    cost = models.PositiveIntegerField()

    # URL in the provider's domain
    url = models.URLField()

    def __unicode__(self):
        return self.name


class Constrains (models.Model):
    "Money and time constrains on a individual item buy."

    # How much the consumer is willing to pay for shipping, in cents.
    max_shipping_cost = models.PositiveIntegerField()
