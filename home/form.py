from django import forms

from home.models import Product, Bidders


class createProduct(forms.ModelForm):
    product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'product name'}))
    category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'catagory of product'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','placeholder': 'product description'}))
    minimum_price = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'your minimum price'}))
    start_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'yyyy-mm-dd'}))
    duration = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'enter in days e.g. 5'}))
    class Meta:
        model = Product
        fields = ['product_name', 'image', 'category', 'description', 'minimum_price', 'start_date', 'duration']


class BidForm(forms.ModelForm):
    class Meta:
        model = Bidders
        fields = ['bid_amount', ]
