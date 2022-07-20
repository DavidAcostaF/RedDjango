from django.urls import path

from apps.red.api.api import ComentarioAPIView

urlpatterns = [
    path('comentarios/',ComentarioAPIView.as_view(),name='comentarios_api')
]
