
from django.db import models
from django.contrib.auth.models import User
from distribuidora_app.models import CuentaModel


# Create your models here.

class NotificacionModel(models.Model):
    asunto = models.CharField(verbose_name='Asunto',max_length=100,blank=False,null=False)
    descripcion = models.CharField(verbose_name='Descripcion',max_length=200,blank=False,null=False)
    leida= models.BooleanField(default=False,blank=False,null=False)
    usuario_creador = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False,verbose_name='Creo')
    cuenta_notificada = models.ForeignKey(CuentaModel,on_delete=models.CASCADE,blank=False,null=False,verbose_name='Notifica a:')
    TYPE_CHOICES = (
        ('1','ALTA'),
        ('2','MEDIA'),
        ('3','BAJA')
        )

    prioridad=models.CharField(verbose_name='Prioridad',choices=TYPE_CHOICES,max_length=10,blank=False,null=False)
    state=models.BooleanField(default=True)
    created_date= models.DateField('Fecha de creación',auto_now=False, auto_now_add=True)
    modified_date= models.DateField('Fecha de modificación',auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name='Notificacion'
        verbose_name_plural='Notificaciones'
    
    def __str__(self):
        return self.asunto
    
    def json(self):
        data={
            'asunto':self.asunto,
            'descripcion':self.descripcion,
            'usuario_creador':self.usuario_creador,
            'cuenta_notificada':self.cuenta_notificada,
            'prioridad':self.prioridad
        }
        return data

    def marcar_leida(self):
        self.leida=True 
    
