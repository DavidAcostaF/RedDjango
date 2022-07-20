from rest_framework import serializers

from apps.red.models import PostComentarios


class ComentariosSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostComentarios
        fields = '__all__'
    
    def to_representation(self, instance):
        #print(instance.post.id)
        return {
            'id': instance.id,
            'usuario':instance.usuario.id,
            'first_name':instance.usuario.first_name,
            'last_name':instance.usuario.last_name,
            'perfil':instance.usuario.image.url if instance.usuario.image != '' else '',
            'post': instance.post.id,
            #'post_image':instance.post.imagen.url if instance.post.imagen != '' else '',
            'comentario': instance.comentario,
            'respuestas': instance.comentario_self.post.id if instance.comentario_self != None else ''
            # 'like': instance.like,
        }