from django import forms
from .models import Product


class OrderForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Produkt"
    )
    quantity = forms.IntegerField(
        min_value=1,
        label="Ilość"
    )