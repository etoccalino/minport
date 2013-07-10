from django.core.urlresolvers import reverse
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
        self.helper.add_input(Submit('submit', 'Listo'))


class EditItemOrderForm (ItemOrderForm):

    def __init__(self, *args, **kwargs):
        super(EditItemOrderForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('base:edit_item_order',
                                          args=(self.instance.pk,))


class NewItemOrderForm (ItemOrderForm):

    def __init__(self, *args, **kwargs):
        super(NewItemOrderForm, self).__init__(*args, **kwargs)
        self.helper.form_action = 'base:new_item_order'
