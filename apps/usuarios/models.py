from django.db.models import Q
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser, BaseUserManager,PermissionsMixin


# Create your models here.


class Usuario(AbstractUser):
    first_name = models.CharField("first name", max_length=150, blank=False,null=False)
    last_name = models.CharField("last name", max_length=150, blank=False,null=False)

    image = models.ImageField('Imagen de Perfil',upload_to='perfil/',default='default.png',blank = False,null = False)
    amigos = models.ManyToManyField(to='self',symmetrical=False,blank = True)#,related_name='amigo'
    portada = models.ImageField('Portada Muro',upload_to='portada/',blank = True,null = True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        if self.first_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{self.username}'

class ThreadManager(models.Manager):
    def by_user(self,**kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person = user) | Q(second_person = user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs

class Thread(models.Model):
    first_person = models.ForeignKey(Usuario,on_delete=models.CASCADE,null = True,blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(Usuario,on_delete=models.CASCADE,null = True,blank=True, related_name='thread_second_person')
    
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person','second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE,null = True,blank=True, related_name='chatmessage_thread')
    user = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateField(auto_now_add=True)


