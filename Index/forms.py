from .models import Usuario
from django import forms

class CSVUploadForm(forms.Form):
    file = forms.FileField(label="Selecciona un archivo CSV")

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'