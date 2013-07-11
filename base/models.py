from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User


class Consumer (User):
    class Meta:
        proxy = True

    @property
    def package(self):
        return self.package_set.get(bought=False)

    def shipping_contribution_relative(self):
        ratio = Decimal(0)
        total = self.package.shipping_cost()
        if total:
            ratio = self.shipping_contribution() / total
        return Decimal(100) * ratio

    def cost_contribution_relative(self):
        items_cost = self.package.items_cost()
        if not items_cost:
            return Decimal(0)
        return self.package.consumer_items_cost() / items_cost

    def shipping_contribution(self):
        total = self.package.shipping_cost()
        return total * self.cost_contribution_relative()

    def __unicode__(self):
        return self.get_full_name()


class Package (models.Model):
    "Each consumer should have exactly one package with bought==False"

    # Who can buy the package.
    consumer = models.ForeignKey(Consumer)

    # Whether this package has been bought.
    bought = models.BooleanField(default=False)

    def buy(self):
        "Mark this package as bought and replace with a new one."
        self.bought = True
        self.save()
        new_package = Package(consumer=self.consumer)
        item_orders = ItemOrder.objects.filter(bought=False)
        for item in item_orders:
            new_package.item_orders.add(item)
        new_package.save()

    def consumer_items_cost(self):
        "The cost in the package which represents the consumer item orders."
        return sum([order.total_cost() for order in self.item_orders.all()
                    if order.consumer == self.consumer])

    def items_cost(self):
        return sum([order.total_cost() for order in self.item_orders.all()])

    def shipping_cost(self):
        return Decimal(20.0)

    def total_cost(self):
        return self.items_cost() + self.shipping_cost()


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

    # URL in the provider's domain
    url = models.URLField(blank=True)

    # Whether this item order has been bought.
    #
    # It's an model attribute to allow filtering, but it's really a property:
    # self.bought == self.packages.filter(bought=True).exists()
    bought = models.BooleanField(default=False, editable=False)

    # Packages this item is presently included in.
    packages = models.ManyToManyField(Package, related_name='item_orders',
                                      editable=False)

    def total_cost(self):
        "Total cost of the order (no discounts applied)."
        return self.item_cost * self.quantity


# Tie in the package life cycle to that of the Consumer/User
#
# When a new user is created, create a "full" package and associate it.
# Users cannot be eliminated, and so packages are never eliminated either.

from django.db.models.signals import post_save


def new_user(sender, instance, created, raw, **kwargs):
    "Assign a full package to the new user"

    # Only for User or its proxy.
    if sender is not Consumer and sender is not User:
        return

    # Only if user is not loaded from fixtures and is new.
    if not raw and created:
        consumer = instance
        if sender is User:
            consumer = Consumer.objects.get(pk=instance.pk)

        package = Package(consumer=consumer)
        item_orders = ItemOrder.objects.filter(bought=False)
        for item in item_orders:
            package.item_orders.add(item)
        package.save()
post_save.connect(new_user, weak=False, dispatch_uid="new_user_new_package")
