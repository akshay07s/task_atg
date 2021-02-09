from .models import URLModel
from django import forms

class URLForm(forms.ModelForm):
    class Meta:
        model = URLModel
        fields = ['url']