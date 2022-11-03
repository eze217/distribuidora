
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

    def creo_grupo_permisos(self):
         #**************************
            # Creo grupos de perfiles

            #grupo empresa
            empresa_permisos=Group.objects.create(name="empresa")
            #permisos para el admin empresa

            permisos_admin= ['view_productomodel', 'change_almacenstockmodel','view_notificacionmodel', 'change_pedidodetallemodel', 
            'delete_productoenventa', 'delete_pedidodetalleclientemodel', 
            'delete_productoalmacenado', 'add_user', 'add_pedidomodel', 
            'add_productoenventa', 'delete_pedidodetallemodel', 
            'view_almacenstockmodel', 'add_entregamodel', 'add_cuentamodel',
            'view_productoalmacenado', 'add_productoalmacenado', 'add_perfil', 
            'change_cuentamodel', 'delete_cuentamodel', 'add_almacenstockmodel','delete_notificacionmodel', 'view_pedidodetallemodel', 'add_productomodel',
            'delete_productomodel', 'view_cuentamodel', 'view_entregamodel', 'change_notificacionmodel', 'change_entregamodel', 'change_productoalmacenado', 
            'change_productomodel', 'view_pedidodetalleclientemodel', 'view_pedidomodel', 
            'view_productoenventa', 'change_pedidodetalleclientemodel', 'delete_entregamodel',
            'change_productoenventa', 'add_pedidodetalleclientemodel', 
            'add_pedidodetallemodel', 'delete_almacenstockmodel', 'change_pedidomodel', 
            'delete_pedidomodel']

            for permiso in permisos_admin:           
                empresa_permisos.permissions.add(Permission.objects.get(codename=permiso))
            
            

            #Grupo proveedor
            proveedor_permisos=Group.objects.create(name='proveedor')
            
            permisos_proveedor=[]

            proveedor_permisos.permissions.set(permisos_proveedor)
            
            
            
            #Grupo cliente
            cliente_permisos=Group.objects.create(name='cliente')

            permisos_cliente=[]

            cliente_permisos.permissions.set(permisos_cliente)

    
    def creoPrimerLogin(self,email,password,nombre,apellido):
        try:
            #creo admin
            admin =User.objects.create_user(username='admin',email=email,password=password)
            admin.is_staff= True
            admin.is_active=True
            admin.first_name=nombre
            admin.last_name=apellido
            admin.save()

            cuenta_admin= CuentaModel.objects.create(name='Distribuidora',domicilio='',telefono='',nro_identificacion='')

            Perfil.objects.create(usuario= admin, cuenta= cuenta_admin)


            #creo super-user

            super_user= User.objects.create_superuser(username='superAdmin',email=None,password='Fase1234-')

            Perfil.objects.create(usuario= super_user, cuenta= cuenta_admin)

            #Creo grupo de usuarios y agrego permisos al admin

            self.creo_grupo_permisos()

            grupo=Group.objects.get(name="empresa")

            admin.groups.add(grupo)
            
            

            self.primer_login=True



            return admin
        except:
            self.primer_login=False
            pass
