
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from distribuidora_app.models import ProveedorModel



class Perfil (models.Model):  
    usuario= models.OneToOneField(User, on_delete=models.CASCADE)
    is_proveedor=models.BooleanField(null=True,blank=True)
    is_cliente=models.BooleanField(null=True,blank=True)
    proveedor= models.ForeignKey(ProveedorModel,on_delete=models.CASCADE, blank=True, null=True,default='')

