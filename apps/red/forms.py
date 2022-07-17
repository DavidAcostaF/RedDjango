from cProfile import label
from django import forms
from . import models


class FormPost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ["contenido", "imagen", "disponible"]
        labels = {
            "contenido": "Contenido de la publicacion",
            "imagen": "Imagen de la publicacion",
            "disponible": "Privacidad de la publicacion",
        }
        widgets = {
            "contenido": forms.TextInput(attrs={"class": "form-control"}),
            "imagen": forms.FileInput(attrs={"class": "form-control form-control-lg"}),
            "disponible": forms.Select(attrs={"class": "form-control"}),
        }


class FormCompartido(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ["contenido"]
        labels = {"contenido": "Contenido del compartido"}
        widgets = {"contenido": forms.TextInput(attrs={"class": "form-control"})}


# contenido = forms.CharField(
#     label = 'Contenido del compartido',
#     widget = forms.Textarea(attrs={
#         'class':'form-control'
#     })
# )
