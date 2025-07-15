from django import forms
from .models import Order

# Form for adding items to the cart
# We use a tuple for QUANTITY_CHOICES as it's a fixed list
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)] # Quantities from 1 to 20

class CartAddProductForm(forms.Form):
    # Quantity field with choices
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int, # Convert input to integer
                                empty_value=1, # Default value if nothing selected
                                widget=forms.Select(attrs={'class': 'form-select rounded-md shadow-sm'}) # Tailwind class
                            )
    # Update field (hidden) to indicate if quantity should be updated or added
    update = forms.BooleanField(required=False,
                                 initial=False,
                                 widget=forms.HiddenInput)

# Form for the checkout process
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm w-full'}),
            'email': forms.EmailInput(attrs={'class': 'form-input rounded-md shadow-sm w-full'}),
            'address': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm w-full'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm w-full'}),
            'city': forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm w-full'}),
        }
