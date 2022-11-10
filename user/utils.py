from django.contrib.auth.models import User,Group,Permission
from distribuidora_app.models import CuentaModel
from .models import PrimerLoginModel,Perfil



'''
************************************************************************************************

                            Modelo usado para control del primer login 
                            y generación automatica del usuario y cuenta Admin

************************************************************************************************
'''

def creo_grupo_permisos():
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
            
            permisos_proveedor=['view_productomodel', 'view_pedidomodel', 'change_productomodel', 'change_pedidomodel', 'view_entregamodel', 'delete_productomodel', 'view_notificacionmodel', 'add_productomodel']

            for permiso in permisos_proveedor:           
                proveedor_permisos.permissions.add(Permission.objects.get(codename=permiso))
                
            #Grupo cliente
            cliente_permisos=Group.objects.create(name='cliente')

            permisos_cliente=['add_pedidomodel', 'add_entregamodel', 'delete_entregamodel', 'view_notificacionmodel', 'change_entregamodel', 'view_pedidodetalleclientemodel', 'add_pedidodetalleclientemodel', 'view_pedidomodel', 'view_entregamodel']
            
            for permiso in permisos_cliente:           
                cliente_permisos.permissions.add(Permission.objects.get(codename=permiso))
            
            
            return True
    
def creoPrimerLogin(email,password,nombre,apellido):
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
 
        creo_grupos=creo_grupo_permisos()
 
        grupo=Group.objects.get(name="empresa")

        admin.groups.add(grupo)


        return admin
    except:
       
        pass