from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser, BaseUserManager,PermissionsMixin

# Create your models here.


class Usuario(AbstractUser):
    image = models.ImageField('Imagen de Perfil',upload_to='perfil/',default='default.png',blank = False,null = False)
    amigos = models.ManyToManyField(to='self',symmetrical=False,blank = True)#,related_name='amigo'
    portada = models.ImageField('Portada Muro',upload_to='portada/',blank = True,null = True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        if self.first_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.username}'


# class Amigos(models.Model):
#     usuario = models.ForeignKey(Usuario,on_delete = models.CASCADE,related_name='usuarios')
#     amigos = models.ManyToManyField(Usuario,related_name='amigo')
#     agregado = models.BooleanField(default=False)

