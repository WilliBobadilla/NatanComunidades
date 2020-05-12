from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Ingrese un usuario",                
                "class": "form-control"
            }
        ))

    apellido = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Ingrese su apellido",                
                "class": "form-control"
            }
        ))

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Ingrese un correo",                
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Ingrese una clave",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Repita la clave",                
                "class": "form-control"
            }
        ))

# codigo para las opciones de los roles

    OPTIONS_CHOICES= [
    ('registrador', 'Registrador'),
    ('administrador','Administrador'),
    ('distribuidor','Distribuidor'),
    ]

    Roles = forms.CharField(
        widget=forms.Select(         
            attrs={                
                "class": "form-control"
            },
            choices=OPTIONS_CHOICES,
        ))



    class Meta:
        model = User
        fields = ('username','apellido', 'email', 'password1', 'password2','Roles')
        
from .models import Donacion


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = Donacion
        fields = ['donante','imagen']