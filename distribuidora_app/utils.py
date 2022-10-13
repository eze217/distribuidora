from ast import Return
from django.db.models import Sum
from distribuidora_app.models import AlmacenStockModel, EntregaModel, PedidoDetalleClienteModel, PedidoDetalleModel, PedidoModel, ProductoEnVenta,ProductoModel,ProductoAlmacenado
from notificacion.models import NotificacionModel






def cantidadPorProducto(almacen=None):#recibo el queryset con de la clase almacenstokmodel

   
    #controlo que envie un arg de tipo correcto
    if almacen != None and type(almacen)!=EntregaModel:
        
        return None


    anulaciones=AlmacenStockModel.objects.filter(movimiento='INGRESO',nro_pedido__usuario__perfil__is_cliente= True).aggregate(cantidad_total=Sum('cantidad')) 
    #stock por productos, trae un diccionario con id prod y cantidad total en stock
    if almacen == None:
        #si no llega almacen traigo todos
        consulta_Ingreso = AlmacenStockModel.objects.filter(movimiento='INGRESO').values('producto').annotate(Sum('cantidad'))
        consulta_Egreso = AlmacenStockModel.objects.filter(movimiento='EGRESO').values('producto').annotate(Sum('cantidad'))
        anulaciones['cantidad_total']=0
    else:#si envio un almacen busco por ese en especifico
        consulta_Ingreso= AlmacenStockModel.objects.filter(state=True,almacen=almacen,movimiento='INGRESO').values('producto').annotate(Sum('cantidad'))
        consulta_Egreso= AlmacenStockModel.objects.filter(state=True,movimiento='EGRESO').values('producto').annotate(Sum('cantidad'))
        #Anulaciones se descuenta solo cuando se filtra por almacen ya que en INGRESO de la anulacion no se marca almacen, entonces queda por debajo.
        

    #armo nueva lista trayendo los productos segun ID

    lista_total_productos=[]
   
    for producto in consulta_Ingreso:   
        if len(consulta_Egreso) > 0 :
            encuentra=False
            for egreso in consulta_Egreso:
                
                if producto['producto'] == egreso['producto']: 
                    lista_total_productos.append({'producto':ProductoModel.objects.get(id=producto['producto']),'cantidad':producto['cantidad__sum']- (egreso['cantidad__sum']-anulaciones['cantidad_total']) })
                    encuentra=True
                 
                    
            if not encuentra:
                lista_total_productos.append({'producto':ProductoModel.objects.get(id=producto['producto']),'cantidad':producto['cantidad__sum']})

        else:
            lista_total_productos.append({'producto':ProductoModel.objects.get(id=producto['producto']),'cantidad':producto['cantidad__sum']})

    return lista_total_productos


def verificoCantidad_EnVenta(lista_prodVta=None):

    if lista_prodVta== None:
        lista_prodVta=ProductoEnVenta.objects.filter(state=True).all().order_by('producto')

    stock= cantidadPorProducto()#traigo stock en almacen

    list_prod_venta=[]
    #verificar est recorrido porque me trae mas de 1 vez los productos si los pongo mas de 1 vez a la venta
    
    for producto in stock:

        for enVta in lista_prodVta:
            if producto['producto'] == enVta.producto :
                if producto['cantidad'] >= enVta.cantidad_venta:
                    list_prod_venta.append(enVta)
                elif producto['cantidad'] <= enVta.cantidad_venta and producto['cantidad']>0:
                    enVta.cantidad_venta = producto['cantidad']
                    enVta.save()
                    list_prod_venta.append(enVta)

                
    
    return list_prod_venta



def ProductosNOenVenta():
    #traigo los productos en venta
    productosEnVenta= verificoCantidad_EnVenta()
    #traigo el stock completo (ingreso-egreso)
    stock_general= cantidadPorProducto()

    #lista para almacenar los productos
    list_prod_almacenados=[]


    for producto in stock_general:
        #del stock veo cuales esta en venta
      
        cantidad_almacenada = producto['cantidad']
        for enVta in productosEnVenta:
            #si esta a la venta
     
            
            if producto['producto'] == enVta.producto and enVta.state:# el estado me permite tener un producto en particular a la venta(por el costo diferenciado)
                cantidad_almacenada -= enVta.cantidad_venta

        if cantidad_almacenada >0:
            list_prod_almacenados.append(ProductoAlmacenado.objects.get_or_create(producto=producto['producto'],cantidad=cantidad_almacenada))

    return list_prod_almacenados



#Funcion control cambio estado

def cambio_estado_pedido(estado_actual,pedido):

    '''
        Como al generar el formulario con la instancia no obtengo el estado "anterior" pido en los parametros
        me envien el estado "actial/anterior" al cambio para hacer los filtros correspondientes
    '''

    nuevo_estado=pedido.estado

    #Separo los cambios si el pedido es de un cliente o de la empresa a un proveedor

    #===========================CAMBIO ESTADO PEDIDOS DE CLIENTES ========================
    if pedido.usuario.perfil.is_cliente:
        #codigo para cliente
        detalle_Pedido= PedidoDetalleClienteModel.objects.filter(pedido=pedido).all()
      
        if estado_actual == 'ANULADO':
          
            #si esta anulado ya no se puede cambiar / como necesita tomar el stock de nuevo puede que ya no tenga mas.
            
            return False
        if nuevo_estado == 'ANULADO' and estado_actual!= 'ANULADO':
        
            #Si lo anulo revierto los movimientos y devuelvo las cantidades al stock
            for producto in detalle_Pedido:
                producto.producto_venta.cantidad_venta += producto.cantidad
                producto.producto_venta.save() 
                AlmacenStockModel.objects.create(cantidad=producto.cantidad,producto=producto.producto_venta.producto,movimiento='INGRESO',nro_pedido=producto.pedido)
            
        
    else:
        #===========================CAMBIO ESTADO PARA PEDIDOS A PROVEEDORES ========================
        detalle_Pedido= PedidoDetalleModel.objects.filter(pedido=pedido).all()
        #Paso a Entregado, genero stock
        if nuevo_estado == 'ENTREGADO' and estado_actual!= 'ENTREGADO':#Lo pongo entregado
            for stock in detalle_Pedido:
                #Movimiento ingreso porque agrega a stock
                agrego_stock= AlmacenStockModel.objects.create(cantidad=stock.cantidad,producto=stock.producto,movimiento='INGRESO',almacen=pedido.datos_entrega,nro_pedido=pedido)

        elif estado_actual== 'ENTREGADO' and nuevo_estado != 'ENTREGADO':#Lo saco de Entregado
            #Lo saco de entregado, debo eliminar el stock
            #Elimino directamente el movimiento, ya que es un "entregado" falso, por eso no genero un mov. de EGRESO
            stock_previo= AlmacenStockModel.objects.filter(nro_pedido=pedido).all()
            stock_previo.delete()    
    
    

    return True