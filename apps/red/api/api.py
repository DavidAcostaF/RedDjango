from rest_framework.views import APIView
from rest_framework.response import Response
from itertools import chain

from apps.red.models import PostComentarios,Post
from apps.red.api.serializers import ComentariosSerializer


class ComentarioAPIView(APIView):

    def get(self,request):
        #pk = request.query_params['pk']
        post = request.query_params['id']
        comentarios = PostComentarios.objects.filter(post = post)
        comentarios_serializer = ComentariosSerializer(comentarios,many = True)
        return Response(comentarios_serializer.data)
        
        # user = request.user
        # amigos = user.amigos.all()
        # self_posts = user.post_set.all()
        # publicaciones = Post.objects.filter(usuario__in = amigos)
        # result_list = list(chain(publicaciones, self_posts))
        # comentarios = PostComentarios.objects.filter(post__in = result_list)