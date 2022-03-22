from django import forms
from django.forms import TextInput,FileInput,Select,EmailInput,PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import *



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,label='Kullanıcı Adı')
    password = forms.CharField(max_length=100,label='Parola',widget=forms.PasswordInput)



class SearchForm(forms.Form):
    query = forms.CharField(label='Search',max_length=100)



class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'username'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'first_name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'last_name'})
        }
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone','address','city')
        widgets = {
            'phone'   : TextInput(attrs={'class': 'input','placeholder':'phone'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'address'}),
            'city': TextInput(attrs={'class': 'input', 'placeholder': 'city'})
        }
