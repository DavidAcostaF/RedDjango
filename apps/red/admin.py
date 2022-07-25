from django.contrib import admin
from .models import Notificaciones, Post,PostGuardados,PostComentarios
# Register your models here.

admin.site.register(Post)
#admin.site.register(PostReacciones)
admin.site.register(PostGuardados)
admin.site.register(PostComentarios)
admin.site.register(Notificaciones)
