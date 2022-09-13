from django.db.models import Sum
from distribuidora_app.models import AlmacenStockModel, EntregaModel, ProductoEnVenta,ProductoModel



def cantidadPorProducto(almacen=None):#recibo el queryset con de la clase almacenstokmodel

   
    #controlo que envie un arg de tipo correcto
    if almacen != None and type(almacen)!=EntregaModel:
        
        return None

    #stock por productos, trae un diccionario con id prod y cantidad total en stock
    if almacen == None:
        #si no llega almacen traigo todos
        consulta_Ingreso = AlmacenStockModel.objects.filter(movimiento='INGRESO').values('producto').annotate(Sum('cantidad'))
        consulta_Egreso = AlmacenStockModel.objects.filter(movimiento='EGRESO').values('producto').annotate(Sum('cantidad'))

    else:#si envio un almacen busco por ese en especifico
        consulta_Ingreso= AlmacenStockModel.objects.filter(state=True,almacen=almacen,movimiento='INGRESO').values('producto').annotate(Sum('cantidad'))
        consulta_Egreso= AlmacenStockModel.objects.filter(state=True,movimiento='EGRESO').values('producto').annotate(Sum('cantidad'))
    #armo nueva lista trayendo los productos segun ID

    lista_total_productos=[]
   
    for producto in consulta_Ingreso:   
        if len(consulta_Egreso) > 0 :
            encuentra=False
            for egreso in consulta_Egreso:
                
                if producto['producto'] == egreso['producto']: 
                    lista_total_productos.append({'producto':ProductoModel.objects.get(id=producto['producto']),'cantidad':producto['cantidad__sum']- egreso['cantidad__sum'] })
                    encuentra=True
                 
                    
            if not encuentra:
                lista_total_productos.append({'producto':ProductoModel.objects.get(id=producto['producto']),'cantidad':producto['cantidad__sum']})

        else:
            lista_total_productos.append({'producto':ProductoModel.objects.get(id=producto['producto']),'cantidad':producto['cantidad__sum']})

    return lista_total_productos


def verificoCantidad_EnVenta(lista_prodVta=None):

    if lista_prodVta== None:
        lista_prodVta=ProductoEnVenta.objects.filter(state=True).all()

    stock= cantidadPorProducto()
    list_prod_venta=[]
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

    productosEnVenta= verificoCantidad_EnVenta()

    stock= cantidadPorProducto()
    list_prod_venta=[]
    for producto in stock:
        for enVta in productosEnVenta:
            if producto['producto'] == enVta.producto :
                if producto['cantidad'] >= enVta.cantidad_venta:
                    #crear tabla par aguardar los pendientes de venta tabla igual a la otra
                    list_prod_venta.append(enVta)
                elif producto['cantidad'] <= enVta.cantidad_venta and producto['cantidad']>0:
                    enVta.cantidad_venta = producto['cantidad']
                    enVta.save()
                    list_prod_venta.append(enVta)

                
    
    return list_prod_venta


