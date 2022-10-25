
from email.policy import default
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from distribuidora_app.models import CuentaModel



class Perfil (models.Model):  
    usuario= models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    is_proveedor=models.BooleanField(null=True,blank=True,default=False)
    is_cliente=models.BooleanField(null=True,blank=True,default=False)
    cuenta= models.ForeignKey(CuentaModel,on_delete=models.CASCADE, blank=True, null=True,default=None)

