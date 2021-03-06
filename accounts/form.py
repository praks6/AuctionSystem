from django import forms
from .models import User
from django.utils import timezone


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'eg.ram@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'eg.ram@gmail.com'}))
    fullName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ram kumar kc'}))
    contactNo = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '9843xxxxx', 'max': 10}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ktm'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label="Password Confirmation")

    class Meta:
        model = User
        fields = ['email', 'fullName', 'contactNo', 'address', 'password']

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password2 = cleaned_data.get('password2')
        password = cleaned_data.get('password')
        if password != password2:
            self.add_error('password2', 'Password does not match!! Please enter same password')
        return cleaned_data

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user

