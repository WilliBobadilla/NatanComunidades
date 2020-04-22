from django import forms
from .models import Donacion


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = Donacion
        fields = ['imagen']