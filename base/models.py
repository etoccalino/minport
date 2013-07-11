from django.db import models
from django.contrib.auth.models import User


class Consumer (User):
    class Meta:
        proxy = True

    @property
    def package(self):
        return self.package_set.get(bought=False)

    def __unicode__(self):
        return self.get_full_name()


class Package (models.Model):
    "Each consumer should have exactly one package with bought==False"

    # Who can buy the package.
    consumer = models.ForeignKey(Consumer)

    # Whether this package has been bought.
    bought = models.BooleanField(default=False)


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
        "Total cost of the order (no discounts applied), in cents."
        return self.item.cost * self.quantity


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
