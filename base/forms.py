from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ItemOrderForm (forms.Form):
    # Descriptive name of the item to buy.
    item_name = forms.CharField(max_length=30)

    # Cost of an individual item, in cents.
    item_cost = forms.FloatField(min_value=0)

    # Number of items to buy.
    quantity = forms.IntegerField(min_value=1)

    # URL in the provider's domain
    url = forms.URLField()

    # How much the consumer is willing to pay for shipping, in cents.
    max_shipping_cost = forms.FloatField(min_value=1)

    def __init__(self, *args, **kwargs):
        super(ItemOrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'base:new_item_order'
        self.helper.add_input(Submit('submit', 'Listo'))
