from django import models
from django.contrib.auth.models import User


class Consumer (User):
    pass


class Package (models.Model):

    # Who bought the package. NULL if package has not been bought.
    buyer = models.ForeignKey(Consumer, related='packages_bought', null=True)


class ItemOrder (models.Model):
    "An intention to buy a number of a particular item."

    # Who ordered this item.
    consumer = models.ForeignKey(Consumer, related_name='item_orders')

    # Number of items to buy.
    quantity = models.PositiveInteger(default=1)

    item = models.OneToOneField('Item')

    # Consumer constrains for this item order.
    constrains = models.OneToOneField('Constrains')

    # Whether this item order has been bought.
    #
    # TRUE means the 'package' attribute should be used. FALSE means the item
    # order is still potential, and the 'potential_packages' attribute should
    # be used instead.
    bought = models.Boolean(default=False)
    package = models.ForeignKey(Package, related='item_orders', null=True)
    potential_packages = models.ManyToManyField(
        Package, related='potential_item_orders')

    def total_cost(self):
        "Total cost of the order (no discounts applied)."
        return self.cost * self.quantity


class Item (models.Model):
    "An item in the provider that consumers can buy."

    # Descriptive name of the item to buy.
    name = models.CharField(max_length=30, blank=False)

    # Cost of an individual item.
    cost = models.PositiveNumber()

    # URL in the provider's domain
    url = models.URLField()


class Constrains (models.Model):
    "Money and time constrains on a individual item buy."

    # How much the consumer is willing to pay for shipping.
    max_shipping_cost = models.PositiveInteger()
