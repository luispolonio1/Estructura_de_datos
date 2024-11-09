from .models import Usuario
from django import forms

class CSVUploadForm(forms.Form):
    file = forms.FileField(label="Selecciona un archivo CSV")

    def clean_file(self):
        archivo = self.cleaned_data['file']
        # Verificar la extensión
        if not archivo.name.endswith('.csv'):
            raise forms.ValidationError("Solo se permiten archivos CSV.")
        # Verificar el tipo MIME (opcional)
        if archivo.content_type != 'text/csv':
            raise forms.ValidationError("El archivo subido no es un archivo CSV válido.")
        return archivo


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'fecha_registro': forms.DateInput(
                attrs={
                    'placeholder': 'Ejemplo: 2024-00-00',
                    'type':'date',
                }
            ),
            'edad': forms.NumberInput(
                attrs={
                    'placeholder': 'Ingrese su Edad',
                }
            ),
           'cedula': forms.TextInput(
                attrs={
                     'placeholder': 'Ingrese su Cedula',
            }
        ),
            'nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Nombre',
                }
            ),
            'apellido': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su Apellido',
                }
            )
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula solo debe contener números.")
        return cedula

    def clean_nombre_apellido(self):
        nombre = self.cleaned_data.get('nombre')
        apellido = self.cleaned_data.get('apellido')
        if not nombre.isalpha() or not apellido.isupper():
            raise forms.ValidationError("El nombre y apellido solo debe contener letras.")
        return nombre,apellido