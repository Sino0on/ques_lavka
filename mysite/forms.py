from django import forms
from .models import ContactRequest, Application

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'form-input', 'required': True}),
            'phone': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Телефон', 'class': 'form-input', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-input', 'required': True}),
        }
