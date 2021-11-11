from django import forms
from .models import *

class CustomerForm(forms.ModelForm):
    def save(self, password, commit=True):
        customer = super(CustomerForm, self).save(commit=False)
        customer.set_password(password)
        if commit:
            customer.save()
        return customer

    class Meta:
        model = Customer
        fields  = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'description')


class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ('name', 'description')
        
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('username', 'total_price')

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ('item_code', 'quantity', 'total_price', 'cart_id')


