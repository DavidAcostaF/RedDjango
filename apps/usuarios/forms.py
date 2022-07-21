from django import forms
from django.contrib.auth.forms import AuthenticationForm

from . import models

class FormularioLogin(AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super(FormularioLogin,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'


class FormularioUsuario(forms.ModelForm):
    password1 = forms.CharField(label = 'Contraseña',widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control inputs',
            'placeholder': 'Ingrese su contraseña...',
            'id': 'password1',
            'required':'required',
        }
    ))

    password2 = forms.CharField(label = 'Contraseña de Confirmación', widget = forms.PasswordInput(
        attrs={
            'class': 'form-control inputs',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            'required': 'required',
        }
    ))

    class Meta:
        model = models.Usuario
        fields = ['username','first_name','last_name','email']
        widgets = {
            'email': forms.EmailInput(
                attrs = {
                    'class': 'form-control inputs',
                    'placeholder': 'Correo Electrónico',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control inputs',
                    'placeholder': 'Ingrese su nombre',
                }
            ),
            'last_name': forms.TextInput(
                attrs = {
                    'class': 'form-control inputs',
                    'placeholder': 'Ingrese sus apellidos',
                }                
            ),
            'username': forms.TextInput(
                attrs = {
                    'class': 'form-control inputs',
                    'placeholder': 'Ingrese su nombre de usuario',
                }
            ),
        }

    def clean_password2(self):
        """ Validación de Contraseña
        Metodo que valida que ambas contraseñas ingresadas sean igual, esto antes de ser encriptadas
        y guardadas en la base dedatos, Retornar la contraseña Válida.
        Excepciones:
        - ValidationError -- cuando las contraseñas no son iguales muestra un mensaje de error
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden!')
        return password2

    def save(self,commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user