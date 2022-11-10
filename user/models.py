
from email.policy import default
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User,Group,Permission
from distribuidora_app.models import CuentaModel



class Perfil (models.Model):  
    usuario= models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    is_proveedor=models.BooleanField(null=True,blank=True,default=False)
    is_cliente=models.BooleanField(null=True,blank=True,default=False)
    cuenta= models.ForeignKey(CuentaModel,on_delete=models.CASCADE, blank=True, null=True,default=None)



'''
************************************************************************************************

                            Modelo usado para control del primer login 
                            y generación automatica del usuario y cuenta Admin

************************************************************************************************
'''


class PrimerLoginModel(models.Model):
    primer_login= models.BooleanField()

    def __str__(self):
        return str(self.primer_login)

