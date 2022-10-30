from operator import indexOf
from notificacion.models import NotificacionModel
from user.models import Perfil
from django.contrib.auth.models import User
from distribuidora_app.models import AlmacenStockModel
from django.db.models import Sum
    

def notificacion_pedido_realizado(pedido):
    '''
    Metodo para crear notificaciones al generar un nuevo pedido. Tanto a proveedores como de clientes
    '''
    #Pedido a proveedor
    if pedido.usuario.is_staff: 
        #pedido de un empleado, solo notifico al proveedor que le hago un pedido
        ASUNTO='Felicidades!!! Te han solicitado un nuevo pedido'
        DESCRIPCION='La empresa Distribuidora te ha realizado un nuevo pedido, puedes ingresar a la seccion pedidos y verlo.\nPor favor, no olvides cambiar el estado.\nMuchas gracias'
        USUARIO_CREADOR=pedido.usuario
        CUENTA_NOTIFICAR=pedido.cuenta
        PRIORIDAD='1'
       
        notifico_proveedor =NotificacionModel.objects.create(asunto=ASUNTO,descripcion=DESCRIPCION,usuario_creador=USUARIO_CREADOR,cuenta_notificada=CUENTA_NOTIFICAR,prioridad=PRIORIDAD)
    #pedidos de clientes
    elif pedido.usuario.perfil.is_cliente:
        #pedido de un cliente a empresa distribuidora, notifico a ambas partes
        asunto='Felicidades!!! Has realizado un nuevo pedido'
        descripcion='Tu pedido Nro. {}, Se generó con exito.\nRecibiras una nueva notificación cuando la empresa lo confirme.\nMuchas gracias'.format(pedido)
        usuario_creador=pedido.usuario
        cuenta_notificada=pedido.cuenta
        prioridad='2'
        
        NotificacionModel.objects.create(asunto=asunto,descripcion=descripcion,usuario_creador=usuario_creador,cuenta_notificada=cuenta_notificada,prioridad=prioridad)

        #notifico a la empresa
        #traigo la cuenta de la empresa
        user_staff=Perfil.objects.filter(usuario__is_staff= True ).first()
        asunto='Tienes un nuevo pedido'
        descripcion='nro de pedido : {}.\nCliente:{}'.format(pedido,pedido.usuario)
        usuario_creador=pedido.usuario
        cuenta_notificada=user_staff.cuenta
        prioridad='2'

        NotificacionModel.objects.create(asunto=asunto,descripcion=descripcion,usuario_creador=usuario_creador,cuenta_notificada=cuenta_notificada,prioridad=prioridad)



def notificacion_cambio_estado(pedido,usuario_cambio):
    '''
        tomo el estado del pedido y notifico a los usuarios sobre su cambio

    '''
    # ===== ESTADOS POSIBLES =====
    ESTADO_UNO='SOLICITADO'
    ESTADO_DOS='CONFIRMADO'
    ESTADO_TRES='EN PREPARACION'
    ESTADO_CUATRO='EN REPARTO'
    ESTADO_CINCO='ENTREGADO'
    ESTADO_SEIS='ANULADO'
    
    #==== VERIFICO ESTADOS ===
    if pedido.estado == ESTADO_SEIS:
        asunto='Tu pedido fue Anulado'
        descripcion= 'Lo sentimos pero el pedido Nro {}. Ha sido anulado. Puede volver a intentar realizar uno nuevo'.format(pedido)
        prioridad='1'
        usuario_creador=usuario_cambio
        
        if usuario_creador.perfil.is_proveedor:
            proveedor= User.objects.filter(is_staff = True, is_superuser=False).first()
            print(proveedor)
            cuenta_notificada=proveedor.perfil.cuenta
        else:
            cuenta_notificada=pedido.cuenta
        

        NotificacionModel.objects.create(asunto=asunto,descripcion=descripcion,usuario_creador=usuario_creador,cuenta_notificada=cuenta_notificada,prioridad=prioridad)

        return True





def control_stock_venta(producto):
   
    ingreso=AlmacenStockModel.objects.filter(producto=producto,movimiento='INGRESO').exclude(nro_pedido__usuario__perfil__is_cliente= True).aggregate(cantidad_total=Sum('cantidad'))
    egreso=AlmacenStockModel.objects.filter(producto=producto,movimiento='EGRESO').aggregate(cantidad_total=Sum('cantidad'))
    anulaciones=AlmacenStockModel.objects.filter(producto=producto,movimiento='INGRESO',nro_pedido__usuario__perfil__is_cliente= True).aggregate(cantidad_total=Sum('cantidad'))
    
    PORCENTAJE_NOTIFICACION = 90
    if anulaciones['cantidad_total'] == None:
        anulaciones['cantidad_total']=0

    ingreso_sin_anulaciones=ingreso['cantidad_total']
    egreso_sin_anulaciones=egreso['cantidad_total']-anulaciones['cantidad_total']

    resto=ingreso_sin_anulaciones-egreso_sin_anulaciones

    porcentaje_restante=(resto*100)/ingreso_sin_anulaciones

    if porcentaje_restante <=PORCENTAJE_NOTIFICACION:
 
        #notifico a la empresa
        #traigo la cuenta de la empresa
        user_staff=Perfil.objects.filter(usuario__is_staff= True ).first()
        asunto='STOCK POR DEBAJO DEL {}%'.format(PORCENTAJE_NOTIFICACION)
        descripcion='El stock del producto {}, ha bajado del porcentaje minimo, realizar un nuevo pedido, STOCK ACTUAL:{} unidades, {} % '.format(producto,resto,porcentaje_restante)
        usuario_creador=user_staff.usuario
        cuenta_notificada=user_staff.cuenta
        prioridad='alta'

        NotificacionModel.objects.create(asunto=asunto,descripcion=descripcion,usuario_creador=usuario_creador,cuenta_notificada=cuenta_notificada,prioridad=prioridad)