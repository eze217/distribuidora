from django.db.models import Sum
from distribuidora_app.models import AlmacenStockModel, EntregaModel,ProductoModel



def cantidadPorProducto(almacen=None):#recibo el queryset con de la clase almacenstokmodel

   
    #controlo que envie un arg de tipo correcto
    if almacen != None and type(almacen)!=EntregaModel:
        
        return None

    #stock por productos, trae un diccionario con id prod y cantidad total en stock
    if almacen == None:
        #si no llega almacen traigo todos
        consulta = AlmacenStockModel.objects.all().values('producto').annotate(Sum('cantidad'))
    else:#si envio un almacen busco por ese en especifico
        consulta= AlmacenStockModel.objects.filter(state=True,almacen=almacen).values('producto').annotate(Sum('cantidad'))
    #armo nueva lista trayendo los productos segun ID

    lista_total_productos=[]

    for producto in consulta:
        lista_total_productos.append({'producto':ProductoModel.objects.get(id=producto['producto']),'cantidad':producto['cantidad__sum']})

    return lista_total_productos