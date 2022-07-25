from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('usuarios/chat/',consumers.ChatConsumer.as_asgi()),
]