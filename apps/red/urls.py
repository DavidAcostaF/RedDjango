from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import static

from . import views

name = 'posts'

urlpatterns = [
    #path('',views.Posts.as_view(),name='posts'),
    path('crear_posts/',views.Posts.as_view(),name='crear_posts'),
    path('editar_post/<int:pk>/',views.EditarPost.as_view(),name='editar_post'),
    path('eliminar_post/<int:pk>/',views.EliminarPost.as_view(),name = 'eliminar_post'),
    path('guardar_post/<int:pk>/',views.GuardarPost.as_view(),name = 'guardar_post'),
    path('post_guardados/',views.PostGuardados.as_view(),name = 'post_guardados'),
    path('borrar_guardado/<int:pk>/',views.BorrarGuardado.as_view(),name = 'borrar_guardado'),
    path('compartir_post/<int:pk>/',views.PostCompartido.as_view(),name = 'compartir_post'),
    path('editar_compartido/<int:pk>',views.PostCompartido.as_view(),name='editar_compartido'),

    path('like/<int:pk>',views.LikePost.as_view(),name='like'),
    path('dislike/<int:pk>',views.Dislikes.as_view(),name='dislike'),

    path('comentar/<int:pk>',views.Comentarios.as_view(),name='comentar'),
    path('like_comentario/<int:pk>',views.LikeComentario.as_view(),name='like_comentario'),
    path('comentarios',views.ListarComentarios.as_view(),name='comentarios'),
    path('contestar/<int:pk>',views.ContestarComentario.as_view(),name='contestar'),
]