from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from models import ItemOrder


class ItemOrderForm (forms.ModelForm):
    class Meta:
        model = ItemOrder

    def __init__(self, *args, **kwargs):
        super(ItemOrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'base:new_item_order'
        self.helper.add_input(Submit('submit', 'Listo'))
