# forms.py
from django import forms
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

class PropertyForm(forms.Form):
    name = forms.CharField(max_length=255)  # Add the name field
    address = forms.CharField(max_length=255)
    bedrooms = forms.IntegerField()
    bathrooms = forms.IntegerField()
    sqft = forms.IntegerField()
    ptype = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10, decimal_places=2)  # Add the price field
    description = forms.CharField(widget=forms.Textarea)

class UserCreationForm(BaseUserCreationForm):
    ROLE_CHOICES = [
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2', 'user_phone', 'user_address', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Set password with hashed value
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.role = self.cleaned_data["role"]
        password = self.cleaned_data["password1"]
        user.password = make_password(password)  # Manually hash the password
        if commit:
            user.save()
        return user