from itertools import chain
from operator import add
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

from . import models
from . import forms
from apps.red.models import Post

class Accounts(TemplateView):
    template_name = 'login.html'

    def get(self,request):
        return render(request,self.template_name,{
            'form2':forms.FormularioUsuario,
            'form1':forms.FormularioLogin
        })

class Login(FormView):
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

    def get(self,request):
        return redirect('index')


def logoutUsuario(request):
    logout(request)
    return redirect('index')


class CrearUsuario(CreateView):
    #model = models.Usuario
    form_class = forms.FormularioUsuario
    template_name = 'login.html'
    # success_url = reverse_lazy('login')

    def post(self,request,*args,**kwargs):
            form = self.form_class(request.POST)
            if form.is_valid():
                nuevo_usuario = models.Usuario(
                    email = form.cleaned_data.get('email'),
                    username = form.cleaned_data.get('username'),
                    first_name = form.cleaned_data.get('first_name'),
                    last_name = form.cleaned_data.get('last_name')
                )
                nuevo_usuario.set_password(form.cleaned_data.get('password1'))
                nuevo_usuario.save()
                return redirect('accounts')
            return HttpResponse(status = 200)

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
        if eliminar:
            user.amigos.remove(agregar)
        else:
            amigo = user.amigos.add(agregar)
        return redirect(request.path)
        #'usuarios:muro',kwargs['nombre'],kwargs['apellido']

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
        print(user)
        # usuario = self.models.objects.get(usuario = user)
        # usuario.objects.add(amigo = seguir)
        # usuario.save()

    def get_object(self,**kwargs):
        pass
        #seguir = kwargs['seguir']
        #print(seguir)
    