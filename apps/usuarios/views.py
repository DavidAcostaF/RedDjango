from itertools import chain
from operator import add
from traceback import print_tb
from turtle import update
from django.views.generic import TemplateView,CreateView,ListView,DeleteView,UpdateView,View,DetailView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.db.models import Q
from django.core.paginator import Paginator

from . import models
from . import forms
from apps.red.models import Post


class Login(FormView):
    template_name = 'login.html'
    form_class = forms.FormularioLogin  
    success_url = reverse_lazy('index')  
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,**kwargs)

    def form_valid(self,form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)


def logoutUsuario(request):
    logout(request)
    return redirect('index')


class CrearUsuario(CreateView):
    model = models.Usuario
    form_class = forms.FormularioUsuario
    template_name = 'register.html'
    #success_url = reverse_lazy('login')

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            nuevo_usuario = models.Usuario(
                email = form.cleaned_data.get('email'),
                username = form.cleaned_data.get('username'),
                first_name = form.cleaned_data.get('first_name'),
                last_name = form.cleaned_data.get('last_name')
            )
            nuevo_usuario.set_password(form.cleaned_data.get('password1'))
            nuevo_usuario.save()
            return redirect('login')
        else:
            print(form.errors)
            return redirect('register')

class ListarUsuarios(ListView):
    model = models.Usuario
    template_name = 'usuarios/listar_usuarios.html'
    def get_queryset(self):
        user = self.request.user
        amigos = user.amigos.all()
        return self.model.objects.all().exclude(Q(usuario__amigos__in = amigos) | Q(username=user.username))#[:1]
        #print(self.model.objects.filter(usuario__in = amigos))
        # return self.model.objects.filter(estado = True)

    def get(self,request):
        return render(request,self.template_name,{'usuarios':self.get_queryset()})

class Muro(DetailView):
    model = Post
    template_name = 'usuarios/muro.html'

    def get(self,request,*args, **kwargs):
        user = request.user
        usuario = self.get_object()
        #post_compartidos = Post.objects.filter(shared_user = usuario)
        post_usuario = self.model.objects.filter(usuario = usuario, estado = True)
        amigo = models.Usuario.objects.filter(usuario__amigos = usuario)
        #result_list = list(chain(post_compartidos,post_usuario))
        paginator = Paginator(post_usuario,10)
        page = request.GET.get('page')
        post_usuario = paginator.get_page(page)
        return render(request,self.template_name,{
        'object_list':post_usuario,
        'usuario':usuario,
        'amigos':amigo
        })

    def get_object(self,**kwargs):
        return models.Usuario.objects.get(first_name = self.kwargs['nombre'], last_name = self.kwargs['apellido'])

    def post(self,request,**kwargs):
        user = request.user
        agregar = self.get_object()
        eliminar = models.Usuario.objects.filter(usuario__amigos = agregar)
        first_person = models.Thread.objects.filter(first_person = user,second_person = agregar)
        second_person = models.Thread.objects.filter(first_person = agregar,second_person = user)
        if eliminar:
            user.amigos.remove(agregar)
            first_person.delete()
        else:
            if second_person:
                print(second_person)
            else:
                models.Thread.objects.create(
                first_person = user,
                second_person = agregar
            )
            user.amigos.add(agregar)

        return redirect(request.path)

class UsuariosAgregados(ListView):
    template_name = 'usuarios/usuarios_seguidos.html'
    def get(self,request):
        user = request.user
        amigos = user.amigos.all()
        return render(request,self.template_name,{'object_list':amigos})

class SeguirUsuario(View):
    model = models.Usuario

    def post(self,request,**kwargs):
        user = request.user
        # usuario = self.models.objects.get(usuario = user)
        # usuario.objects.add(amigo = seguir)
        # usuario.save()

    def get_object(self,**kwargs):
        pass
        #seguir = kwargs['seguir']
        #print(seguir)


class BuscarUsuario(View):
    template_name = 'usuarios/busqueda.html'

    def get(self,request):
        query = request.GET.get('usuario')

        usuarios = models.Usuario.objects.filter(Q(first_name__icontains = query) | Q(last_name__icontains = query))
        publicaciones = Post.objects.filter(Q(contenido__icontains = query))
        context = {
            'usuarios':usuarios,
            'hashtag':publicaciones,
        }
        return render(request,self.template_name,context)

class ConfiguracionPerfil(CreateView):
    model = models.Usuario
    template_name = "configuracion_perfil.html"
    form_class = forms.EditarUsuario

    def get(self,request):
        user = request.user
        datos_usuario = self.form_class(instance= user)
        context = {}
        context['form'] = datos_usuario
        return render(request,self.template_name,context)

    def post(self,request):
        user = request.user
        form = self.form_class(request.POST,request.FILES,instance = user )

        context = {}
        context['form'] = form
        context['form_errors'] = form.errors
        if form.is_valid():
            form.save()
            #return redirect('usuarios:configuracion_perfil')
        else:
            print(form.errors)
        return render(request,self.template_name,context)

class Chat(View):
    template_name = 'usuarios/chat.html'

    def get(self,request):
        threads = models.Thread.objects.by_user(user = request.user).prefetch_related('chatmessage_thread')
        context = {
            'Threads': threads
        }
        return render(request,self.template_name,context)
