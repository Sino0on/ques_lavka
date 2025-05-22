from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    phone = forms.CharField(
        label='Номер телефона',
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': '+996 XXX XX XX XX'})
    )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'placeholder': 'ваша@почта.com'})
    )
    first_name = forms.CharField(
        label='Имя',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'})
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('phone', 'email', 'first_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user


from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'phone', 'email', 'country', 'city', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
