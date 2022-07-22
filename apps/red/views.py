from msilib.schema import ListView
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,CreateView,FormView,ListView,UpdateView,DeleteView,View
from itertools import chain
from django.core.serializers import serialize
from django.db.models import Q
from django.core.paginator import Paginator


from . import models
from . import forms
from apps.usuarios.models import Usuario
from apps.usuarios.mixins import LoginYSuperStaffMixins,ValidarPermisosMixins
# Create your views here.



class Inicio(LoginYSuperStaffMixins,ValidarPermisosMixins,ListView):
    model = models.Post
    template_name = 'index.html'
    
    def get_queryset(self):
        queryset = self.model.objects.filter(estado = True)
        return queryset
    
    def get(self,request):
        user = request.user
        amigos = user.amigos.all()
        self_posts = user.post_set.all()
        publicaciones = self.model.objects.filter(usuario__in = amigos)
        result_list = list(chain(publicaciones, self_posts))
        
        paginator = Paginator(result_list,10)
        page = request.GET.get('page')
        result_list = paginator.get_page(page)
        #comentarios = models.PostComentarios.objects.filter(post__in = result_list)
        ##no se agrega por que no tiene relacion con el post el cual es con el que se filtra
        return render(request,self.template_name,{'object_list':result_list}) 


class Posts(LoginYSuperStaffMixins,ValidarPermisosMixins,CreateView):
    model = models.Post
    form_class = forms.FormPost
    template_name = 'posts/posts.html'
    success_url = reverse_lazy('index')
    
    def post(self,request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            models.Post.objects.create(
                usuario = request.user,
                contenido = form.cleaned_data.get('contenido'),
                imagen = form.cleaned_data.get('imagen'),
                disponible = form.cleaned_data.get('disponible')
            )
        return HttpResponse(status = 204,headers={'HX-Redirect':''}) 
    # def get(self,request):
    #     queryset = self.model.objects.filter(estado = True)
    #     print(queryset)
    #     return render(request,self.template_name,{'object':queryset})

class EditarPost(UpdateView):
    model = models.Post
    form_class = forms.FormPost
    template_name = 'posts/editar_post.html'
    success_url = reverse_lazy('index')

    def get_context_data(self,**kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['username'] = user
        return context


class EliminarPost(DeleteView):
    model = models.Post

    def post(self,request,pk):
        # post = self.model.objects.get(id = pk)
        # post.delete()
        # return HttpResponse(status = 204,headers={'HX-Redirect':''}) 
        # return redirect('index') 
        post = self.model.objects.filter(id = pk)
        #compartido = models.PostCompartido.objects.filter(id = pk)
        if post:
            post.delete()
        else:
            pass
            #compartido.delete()
        return HttpResponse(status = 204,headers={'HX-Redirect':''}) 
        return redirect('index') 

class GuardarPost(View):
    model = models.PostGuardados

    def post(self,request,pk):
        usuario = request.user
        post_id = models.Post.objects.get(id = pk)
        #compartido = models.PostGuardados.objects.filter(id = pk)
        guardado,created = models.PostGuardados.objects.get_or_create(
            usuario = usuario,
            post = post_id
        )
        if created:
            pass
        else:
            guardado.save()
        return HttpResponse(status = 204,headers={'HX-Redirect':''}) 

        # usuario = request.user
        # post_id = models.Post.objects.filter(id = pk)
        # post_compartido = models.PostCompartido.objects.filter(id = pk)
        # print(post_compartido)
        # if post_id:
        #     guardado,created = models.PostGuardados.objects.get_or_create(
        #         usuario = usuario,
        #         post = post_id
        #     )
            
        # guardado,created = models.PostCompartidoGuardado.objects.get_or_create(
        #     usuario = usuario,
        #     post = post_compartido
        # )
        # if created:
        #     pass
        # guardado.save()
        # return HttpResponse(status = 204,headers={'HX-Redirect':''})


class PostGuardados(ListView):
    model = models.PostGuardados
    template_name = 'posts/posts_guardados.html'
    
    def get(self,request):
        usuario = request.user
        guardados = models.PostGuardados.objects.filter(usuario = usuario)
        return render(request,self.template_name,{'guardados':guardados})


class BorrarGuardado(DeleteView):
    model = models.PostGuardados
    def post(self,request,pk):
        post = models.PostGuardados.objects.get(id = pk)
        post.delete()
        return HttpResponse(status = 204,headers={'HX-Redirect':''}) 
        #return redirect('posts:post_guardados')

class PostCompartido(CreateView):
    form_class = forms.FormCompartido
    template_name = 'posts/compartir_post.html'

    def post(self,request,pk):
        post = models.Post.objects.get(id = pk)
        form = self.form_class(request.POST)
        if form.is_valid():
            models.Post.objects.create(
                contenido = form.cleaned_data.get('contenido'),
                shared_post = post,
                disponible = post.disponible,
                usuario = request.user
            )
            post.veces_compartidos += 1
            post.save()
        return HttpResponse(status = 204,headers={'HX-Redirect':''}) 

class EditarCompartido(UpdateView):
    model = models.Post
    form_class = forms.FormCompartido
    template_name = 'posts/editar_compartido.html'
    success_url = reverse_lazy('index')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context



class LikePost(View):
    model = models.Post

    def post(self,request,pk):

        usuario = request.user
        post = models.Post.objects.get(id = pk)
        likes = post.like.all()
        # if likes.count() == 0:
        #     post.dislike.remove(usuario)
        #     post.like.add(usuario)
        # else:
        if post.like.contains(usuario):
            post.like.remove(usuario)
        else:
            post.like.add(usuario)
            post.dislike.remove(usuario)
        return HttpResponse(status = 204)


class Dislikes(View):
    model = models.Post

    def post(self,request,pk):
        usuario = request.user
        post = models.Post.objects.get(id = pk)
        dislikes = post.dislike.all()

        # if dislikes.count() == 0:
        #     post.dislike.add(usuario)
        #     post.like.remove(usuario)
        # else:

        if post.dislike.contains(usuario):
            post.dislike.remove(usuario)
        else:
            post.dislike.add(usuario)
            post.like.remove(usuario)
        return HttpResponse(status = 204)

class Comentarios(View):
    model = models.PostComentarios

    def post(self,request,pk):
        usuario = request.user
        comentario = request.POST.get('comentario')
        post = models.Post.objects.get(id = pk)

        models.PostComentarios.objects.create(
            usuario = usuario,
            post = post,
            comentario = comentario,
        )
        return HttpResponse(status = 204)



class LikeComentario(View):
    model = models.PostComentarios

    def post(self,request,pk):
        usuario = request.user
        post = models.PostComentarios.objects.get(id = pk)
        #comentarios = post.like.all()

        if post.like.contains(usuario):
            post.like.remove(usuario)
        else:
            post.like.add(usuario)
        return HttpResponse(status = 204)

class ContestarComentario(View):
    model = models.PostComentarios

    def post(self,request,pk):
        print(pk)
        comentario = models.PostComentarios.objects.get(id = pk)
        models.PostComentarios.objects.create(
            usuario = request.user,
            comentario_self = comentario,
            comentario = request.POST.get('comentario')
            )
        return HttpResponse(status = 204)

class ListarComentarios(ListView):
    model = models.Post

    def get(self,request):
        user = request.user
        amigos = user.amigos.all()
        self_posts = user.post_set.all()
        publicaciones = self.model.objects.filter(usuario__in = amigos)
        result_list = list(chain(publicaciones, self_posts))
        comentarios = models.PostComentarios.objects.filter(post__in = result_list)
        return HttpResponse(serialize('json', comentarios,use_natural_foreign_keys = True), 'application/json')        
        ##no se agrega por que no tiene relacion con el post el cual es con el que se filtra
        print(comentarios)
        return render(request,self.template_name,{'object_list':result_list,
        'comentarios':comentarios}) 
