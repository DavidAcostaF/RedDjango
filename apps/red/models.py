from django.db import models
from apps.usuarios.models import Usuario
# Create your models here.

privacidad_publicacion = [
    (1,'Público'),
    (2,'Solo yo')
]


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    shared_post = models.ForeignKey(to='self',blank = True,on_delete=models.CASCADE,null=True)
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    contenido = models.TextField('Descripcion',max_length=150,blank=False,null=False)
    imagen = models.ImageField('Imagen post', upload_to='post/',blank = True,null=True)
    disponible = models.IntegerField(null=False,blank=False,choices=privacidad_publicacion,default=privacidad_publicacion[0])
    veces_compartidos = models.IntegerField('Veces compartido',null=True,blank=True,default=0)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField('Fecha de creacion',auto_now=False, auto_now_add=True)
    like = models.ManyToManyField(Usuario,blank=True,related_name='like')
    dislike = models.ManyToManyField(Usuario,blank=True,related_name='dislike')


class PostComentarios(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,blank=True,null=True)
    comentario = models.TextField('Comentario',blank=False,null=False,max_length=200)
    comentario_self = models.ForeignKey(to='self',on_delete=models.CASCADE,blank = True, null = True)
    like = models.ManyToManyField(Usuario,blank=True,related_name='likes')

class PostGuardados(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    

notificacion = [
    (0,'Compartido'),
    (1,'Me gusta'),
    (2,'Comentario'),
]

class Notificaciones(models.Model):
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    accion = models.IntegerField(choices=notificacion,null=False,blank=False)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField('Fecha de creacion',auto_now=False, auto_now_add=True)
