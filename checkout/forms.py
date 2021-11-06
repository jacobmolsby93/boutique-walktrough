from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number', 
                  'street_address1', 'street_address2', 
                  'town_or_city', 'postcode', 'country', 
                  'county',)
    
    def __init__(self, *args, **kwargs):
        """
        Add placeholder and classes, remove auto-generated
        labels and set autofocus on first field
        """

        super().__init__(*args, **kwargs)  # call default init form method to set the form up as like default
        placeholders = {  # a dict of placeholders which will show up in the form field 
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Addres 2',
            'county': 'County'
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True  # setting autofocus attr to the full name field to true 
        for field in self.fields:  # itterating through the form fields and adding a star to the fields that are required.
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder  # setting all the values to the placeholder dict above
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'  # adding a css class 
            self.fields[field].label = False  # removing the form field labels