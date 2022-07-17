from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import static
from . import views 

urlpatterns = [
    path('disponibles/',views.ListarUsuarios.as_view(),name = 'disponibles'),
    path('seguidos/',views.UsuariosAgregados.as_view(),name = 'seguidos'),
    path('muro/<str:nombre>.<str:apellido>/',views.Muro.as_view(),name = 'muro'),
    path('seguir/<str:nombre>/',views.SeguirUsuario.as_view(),name = 'seguir'),

]