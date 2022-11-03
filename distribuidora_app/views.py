
from datetime import datetime
from multiprocessing import context
from unicodedata import name
from django.shortcuts import render,redirect
from django.views import View
from django.http.response import JsonResponse
from django.contrib.auth.models import User,Group,Permission


from distribuidora_app.forms import EntregaCreateForm, ProveedorForm,ProductoAdminForm,ProductoForm,ProductoEditForm
from distribuidora_app.forms import PedidoCreateForm
from distribuidora_app.forms import PedidoEdicionForm
from distribuidora_app.forms import ProductoEnVentaEditForm

from distribuidora_app.models import AlmacenStockModel, PedidoDetalleClienteModel, PedidoDetalleModel, PedidoModel, CuentaModel, ProductoAlmacenado,ProductoModel,EntregaModel,ProductoEnVenta
from distribuidora_app.utils import cantidadPorProducto ,verificoCantidad_EnVenta,ProductosNOenVenta,cambio_estado_pedido
from notificacion.models import NotificacionModel

#NOTIFICACIONES
from notificacion.utils import control_stock_venta, notificacion_cambio_estado, notificacion_pedido_realizado

import json
from user.models import Perfil


def home (request):
    
    if request.method == 'GET':
        if request.user.is_authenticated:
            #print(request.user.get_user_permissions())
            return redirect('home-app')
        return render(request,'landing/index.html',{})


def prohibido(request):
    if request.user.is_authenticated:
        context={
            'HAS_ACCESS':True
        }
        return render(request,'core_template/no_autorizado.html',context)

    


class Home_App(View):
   
    
    def get(self,request,leidas=None,*args,**kwargs):
        HAS_ACCESS=False
        usuario=self.request.user
        if usuario.is_authenticated:
            context= {}
            HAS_ACCESS=True
            if usuario.has_perm('notificacion.view_notificacionmodel'):
                if leidas != None:
                    notificaciones= NotificacionModel.objects.filter(state=True,cuenta_notificada=usuario.perfil.cuenta,leida=True).all().order_by('-prioridad','-id')
                else:
                    notificaciones= NotificacionModel.objects.filter(state=True,cuenta_notificada=usuario.perfil.cuenta,leida=False).all().order_by('-prioridad','-id')
                context['notificaciones']=notificaciones

            context['HAS_ACCESS']= HAS_ACCESS
         
           
            return render(request,'app/home.html',context )
        else:
            return redirect ('landing_home')

# ============================================================== VISTAS PROVEEDORES ================================================================================
class ProveedoresView(View):
    
    def get (self,request,*args,**kwargs):
        HAS_ACCESS:False
        context={}
        usuario = self.request.user
        if usuario.is_authenticated and usuario.is_active:
        
            if usuario.is_staff and usuario.has_perm('distribuidora_app.view_cuentamodel'):

                HAS_ACCESS=True
                form=ProveedorForm()


                #cuentasList= CuentaModel.objects.filter(state=True).all().exclude()
  
                #buscar los proveedores que son solo proveedores
                proveedoresPerfil=Perfil.objects.filter(is_proveedor=True).all()
                
                proveedoresList=[]
                for pp in proveedoresPerfil:
                    if pp.cuenta not in  proveedoresList:
                        proveedoresList.append(pp.cuenta)
               

                

                context['HAS_ACCESS']= HAS_ACCESS          
                context['proveedores_list']=proveedoresList
                
                if  usuario.has_perm('distribuidora_app.add_cuentamodel'):
                    context['form']=form

                return render(request,'app/proveedores/proveedores.html',context )
            else:
                return redirect('no_autorizado')
        else:        
            return redirect ('landing_home')
        
    
    def post(self,request,*args,**kwargs):
       
        usuario = self.request.user
        if usuario.is_authenticated and usuario.is_active:
            if not usuario.is_staff and not usuario.has_perm('distribuidora_app.add_cuentamodel'):
                return redirect('no_autorizado')
            
            formulario= ProveedorForm(request.POST)

            if formulario.is_valid():
                
                nuevo_proveedor= CuentaModel.objects.create(name=formulario.cleaned_data['name'],domicilio=formulario.cleaned_data['domicilio'],telefono=formulario.cleaned_data['telefono'],nro_identificacion=formulario.cleaned_data['nro_identificacion'])
                nuevo_proveedor.save()
                #Creo perfil para la cuenta
                Perfil.objects.create(is_cliente=False,is_proveedor=True,cuenta=nuevo_proveedor)

            return redirect('proveedores' )
        else:
            return redirect ('landing_home')

 

class ProveedorDetalleView(View):
    
    def get(self,request,pk,*args,**kwargs):
        HAS_ACCESS:False
        context={}
        proveedor= CuentaModel.objects.filter(state=True,pk=pk).first()
        usuario=self.request.user
        
        if usuario.is_authenticated and usuario.is_active:
            
            if  usuario.is_staff and usuario.has_perm('distribuidora_app.view_cuentamodel'):
                
                usuarios_cuenta=Perfil.objects.filter( cuenta=proveedor)

                context['HAS_ACCESS']= True
                context['proveedor']= proveedor
                context['usuarios']= usuarios_cuenta

                #si tengo permisos para ver pedidos
                if usuario.has_perm('distribuidora_app.view_pedidomodel'):
                    pedidos_proveedor = PedidoModel.objects.filter(state=True,cuenta=proveedor).order_by('-id')
                    context['pedidos_proveedor']=pedidos_proveedor

                if  usuario.has_perm('distribuidora_app.change_cuentamodel'):
                    form_editable= ProveedorForm(instance=proveedor)            
                    context['form']= form_editable

                return render(request,'app/proveedores/proveedor_detalle.html',context)
            else:
                return redirect('no_autorizado')
        else:
            return redirect('landing_home')
    

    def post(self,request,pk,*args,**kwargs):
        usuario=self.request.user
        proveedor= CuentaModel.objects.filter(state=True,pk=pk).first()

        if usuario.is_authenticated and usuario.is_active:
            if  usuario.is_staff and usuario.has_perm('distribuidora_app.change_cuentamodel'):         
                form_editable= ProveedorForm(request.POST,instance=proveedor)
                if form_editable.is_valid():
                    proveedor = form_editable.save()
                    return redirect('proveedor_detalle', pk=proveedor.pk)
            else:
                return redirect('no_autorizado')

                
        else:
            redirect('landing_home')
    

def proveedorEliminaView(request,pk):
    usuario=request.user
    proveedor= CuentaModel.objects.filter(state=True,pk=pk).first()

    if usuario.is_authenticated and usuario.is_active:
        if  usuario.is_staff and usuario.has_perm('distribuidora_app.delete_cuentamodel'):

            if proveedor == usuario.perfil.cuenta:
                return redirect('proveedor_detalle',pk)
            
            proveedor.state=False
            proveedor.save()

            return redirect('proveedores')
        else:
            return redirect('no_autorizado')
       
    return redirect('landing_home')
  



# ============================================================== VISTAS PRODUCTOS ================================================================================

class ProductosView(View):
      
    def get (self,request,pk=None,*args,**kwargs):
        HAS_ACCESS:False
        usuario = self.request.user
        context={}
        if usuario.is_authenticated and usuario.is_active :
            
            if usuario.has_perm('distribuidora_app.view_productomodel'):
                HAS_ACCESS=True
                
                try:
                    perfil= Perfil.objects.get(usuario=usuario)
                except:
                    perfil=None

                if usuario.is_staff:     
                    productosList= ProductoModel.objects.filter(state=True).all()

                    form_Producto=ProductoAdminForm()
            
                elif perfil.is_proveedor : 
                    
                    productosList= ProductoModel.objects.filter(state=True ,proveedor=perfil.cuenta).all()
                    form_Producto=ProductoForm()
                else:
                    return redirect('no_autorizado')
                
                #Si me envia una pk, y tiene permiso de edicion envio form para editar el producto
            
                if pk != None:
                
                    if usuario.has_perm('distribuidora_app.change_productomodel'):

                        producto_editable = ProductoModel.objects.filter(state=True,pk=pk).first()

                        form_editable=ProductoEditForm(instance=producto_editable)
                        context['form_editable']=form_editable
                        context['producto_editable']=producto_editable.id
        
                    
                #Armado del context
                context['HAS_ACCESS']= HAS_ACCESS
                context['productos_list']=productosList
                if usuario.has_perm('distribuidora_app.add_productomodel'):
                    context['form']=form_Producto        
                    
                
            
                return render(request,'app/productos/productos.html',context )
        
            else:#si no tiene permiso
                return redirect('no_autorizado')       
        else:
            return redirect ('landing_home')
        
    def post (self,request,pk=None,*args,**kwargs):
        usuario = self.request.user
        if usuario.is_authenticated and usuario.is_active:

      
               
            if pk != None:#si hay pk es porque es una edicion
                if usuario.has_perm('distribuidora_app.change_productomodel'):
                    
                    producto_editable = ProductoModel.objects.filter(state=True,pk=pk).first()
                    form_Producto= ProductoEditForm(request.POST,instance=producto_editable)

                    if form_Producto.is_valid():
                        try:#si es proveedor
                            if usuario.perfil.is_proveedor:
                                producto_editable= form_Producto.save(commit=False)
                                producto_editable.proveedor = usuario.perfil.cuenta
                                producto_editable= form_Producto.save()
                            else:
                                producto_editable= form_Producto.save()    
                        except:

                            producto_editable= form_Producto.save()
                else:
                    return redirect('no_autorizado')
            else:#si no hay pk es un producto nuevo
                if usuario.has_perm('distribuidora_app.add_productomodel'):
                    try:
                        if usuario.perfil.is_proveedor:
                            
                            form_Producto=ProductoForm(request.POST)
                        else:
                            form_Producto=ProductoAdminForm(request.POST)
                            
                    except:
                        form_Producto=ProductoAdminForm(request.POST)
                
                    if form_Producto.is_valid():
                        producto= ProductoModel()
                        try:#si es proveedor
                            if usuario.perfil.is_proveedor:
                                producto = form_Producto.save(commit=False)
                                producto.proveedor= usuario.perfil.cuenta
                                producto = form_Producto.save()
                            else: 
                                producto = form_Producto.save()
                            
                        except:

                            producto = form_Producto.save()
                else:
                    return redirect('no_autorizado')
                    
               
         
                
                    
            return redirect('productos')
        
        
        else:
            return redirect ('landing_home')




def productoEliminaView(request,pk):
    usuario=request.user
    producto_eliminar= ProductoModel.objects.filter(state=True,pk=pk).first()

    if usuario.is_authenticated and usuario.is_active:
        if usuario.has_perm('distribuidora_app.delete_productomodel'):
            
            producto_eliminar.state=False
            producto_eliminar.save()

            return redirect('productos')
        else:
            return redirect('no_autorizado')

    
     
    return redirect('landing_home')
  


# ============================================================== VISTAS PEDIDOS ================================================================================

class PedidosView(View):
    
    def get (self,request,*args,**kwargs):
        HAS_ACCESS=False
        usuario = self.request.user
        
        context={}

        if usuario.is_authenticated and usuario.is_active:
            if usuario.has_perm('distribuidora_app.view_pedidomodel'):

                HAS_ACCESS=True

                if usuario.is_staff : #empleados 
                    pedidos_list=PedidoModel.objects.filter(state=True).order_by('-id')#.exclude(estado='ANULADO')
                else :
                    if usuario.perfil.is_proveedor: 
                        #proveedor= Perfil.objects.get(usuario=user)
                        pedidos_list=PedidoModel.objects.filter(state=True,cuenta=usuario.perfil.cuenta).order_by('-id')
                    elif usuario.perfil.is_cliente:
                        pedidos_list=PedidoModel.objects.filter(state=True,usuario=usuario).order_by('-id')
                
                
                context['HAS_ACCESS']= HAS_ACCESS
                context['pedidos_list']=pedidos_list
                
                return render(request,'app/pedidos/pedidos.html',context )
            else:
                return redirect ('no_autorizado')
        else:
            return redirect ('landing_home')


                

class PedidoCreateView(View):
    
    def get (self,request,pk=None,*args,**kwargs):
        HAS_ACCESS=False   
        usuario = self.request.user
        context={}

        if usuario.is_authenticated and usuario.is_active:
            HAS_ACCESS=True
            if usuario.has_perms(['distribuidora_app.add_pedidomodel','distribuidora_app.view_pedidomodel']):

                if usuario.is_staff:#si es empleado
                    if pk != None:
                        proveedor= CuentaModel.objects.get(id=pk)
                        productosList=ProductoModel.objects.filter(state=True,proveedor=proveedor)
                        context['productoList']=productosList
                    else:
                        proveedoresPerfil=Perfil.objects.filter(is_proveedor=True).all()
                        #genero listado de proveedores 
                        proveedoresList=[]
                        for pp in proveedoresPerfil:
                            if pp.is_proveedor:
                                proveedoresList.append(pp.cuenta)
   
                        context['proveedoresList']=proveedoresList
                    #busco mis almacenes
                    entrega=EntregaModel.objects.filter(state=True,cuenta=usuario.perfil.cuenta)
                   
                    context['entrega']=entrega

                elif usuario.perfil.is_cliente:#valido sea cliente, proveedores NO hacen pedidos
                  
                    productosList=ProductoEnVenta.objects.filter(state=True)
                    #busco mis Domicilio entrega Clietne
                    entrega=EntregaModel.objects.filter(state=True,cuenta=usuario.perfil.cuenta)
                    
                    context['entrega']=entrega
                    context['productoList']=productosList
                
                context['HAS_ACCESS']=HAS_ACCESS
                return render(request,'app/pedidos/nuevo_pedido.html',context)
            else:
                return redirect('no_autorizado')     
        else:
            return redirect ('landing_home')

    
              
class PedidosJsonView(View):

    def get(self,request,pk,*args,**kwargs):
        HAS_ACCESS=False   
        usuario = self.request.user

        if usuario.is_authenticated and usuario.is_active:
            if usuario.has_perms(['distribuidora_app.add_pedidomodel','distribuidora_app.view_pedidomodel']):
                HAS_ACCESS=True
                if usuario.is_staff:#si soy empleado
                    #traigo proveedor
                    if pk != None:
                        proveedor = CuentaModel.objects.filter(id=pk).first()

                    productosList= ProductoModel.objects.filter(state=True,proveedor=proveedor)

                    #paso a dict
                    lista_productos=[]
                    for producto in productosList:
                        lista_productos.append(producto.json())           
                else:
                    #Acá debo buscar los productos que tengo en stock, NO desde la tabla productos
                    productosList=ProductoModel.objects.filter(state=True)
                
                context={
                        'data':lista_productos,
                        }
                return JsonResponse(context) 
            else:
                return redirect('no_autorizado')





    def post(self,request,pk=None,*args,**kwargs):
        HAS_ACCESS=False   
        usuario = self.request.user
     
        if usuario.is_authenticated and usuario.is_active:
            HAS_ACCESS=True
            if usuario.has_perm('distribuidora_app.add_pedidomodel'):
                #Respuesta para empleados distribuidora

                if usuario.is_staff:

                    jsonData = json.loads(request.body)
                    metarCode = jsonData.get('Metar') 
                    almacen= jsonData.get('almacen')
                    almacen=EntregaModel.objects.get(id=almacen)
                    #if pk != None:
                    try:
                        error= False
                        #busco proveedor al que se le hace el pedido
                        if pk != None:
                            proveedor_pedido = CuentaModel.objects.get(state=True,id= pk)
                            #Creo el pedido
                            nuevo_pedido = PedidoModel.objects.create(estado='SOLICITADO',cuenta=proveedor_pedido,usuario=usuario,tipo_pedido='COMPRA',datos_entrega=almacen)
                        else:# entro si vengo de crear el producto desde la ventana de proveedores
                            #busco el producto un producto, para obtener el proveedor
                            producto_proveedor=ProductoModel.objects.get(state=True,id= metarCode[0]['id'])
                            #creo pedido
                            nuevo_pedido = PedidoModel.objects.create(estado='SOLICITADO',cuenta=producto_proveedor.proveedor,usuario=usuario,tipo_pedido='COMPRA',datos_entrega=almacen)

                        for pedido in metarCode:

                            id_pedido = pedido['id']
                            cantidad_pedido = pedido['cantidad']
                            costo_pedido =pedido['costo']

                            #traigo producto

                            producto_pedido = ProductoModel.objects.get(state=True, id=id_pedido)
                            #creo el detalle    
                            detalle_pedido= PedidoDetalleModel.objects.create(pedido=nuevo_pedido,cantidad=cantidad_pedido,producto=producto_pedido)
                        
                        #armo el contexto para la respuesta

                        detalle_pedido=PedidoDetalleModel.objects.filter(state=True,pedido=nuevo_pedido)
                        notificacion_pedido_realizado(nuevo_pedido)


                        list_producto_detalle=[]

                        for producto in detalle_pedido:

                            list_producto_detalle.append(producto.json())
                            
                    except:
                        error= True
                    



                    context={
                        'error':error,
                        'data':{'pedido':[nuevo_pedido.json()],
                                'detalle_pedido':list_producto_detalle
                                }
                        }

                   

                    return JsonResponse(context) 

                        
                else:##Respuesta para clientes
                    
                    error=True
                    jsonData = json.loads(request.body)
                    metarCode = jsonData.get('Metar') 
                    almacen= jsonData.get('almacen')
                    almacen=EntregaModel.objects.get(id=almacen)
                    mensaje=''
                    try:
                        error= False
                        #Creo el pedido
                        nuevo_pedido = PedidoModel.objects.create(estado='SOLICITADO',cuenta=usuario.perfil.cuenta,usuario=usuario,tipo_pedido='VENTA',datos_entrega=almacen)
                        
                        #Creo lista para guardar productos que superen cantidad de ser necesario
                        lista_prod_cantMax_para_error=[]

                        #recorro los productos solicitados
                        for pedido in metarCode:

                            id_pedido = pedido['id']
                            cantidad_pedido = int(pedido['cantidad'])
                            costo_pedido =pedido['costo']

                            #traigo producto solicitado
                            producto_pedido = ProductoEnVenta.objects.get(state=True, id=id_pedido)
                            #creo el detalle         
                            #bajo stock en venta
                            #creo lista de error en caso que corresponda
                            
                            if producto_pedido.cantidad_venta >= cantidad_pedido :
                                #si la cantidad solicitada es igual o menor a lo que tengo en stock de venta, creo el detalle
                                #bajo el stock de venta de ese producto
                                producto_pedido.cantidad_venta -= cantidad_pedido
                                producto_pedido.save()
                                detalle_pedido= PedidoDetalleClienteModel.objects.create(pedido=nuevo_pedido,cantidad=cantidad_pedido,producto_venta=producto_pedido)
                                #bajo el stock general creo el movimiento de egreso
                                #Descuento del almacen correspondiente
                                
                                user_staff=Perfil.objects.filter(usuario__is_staff=True).first()
                                almacenes = EntregaModel.objects.filter(cuenta=user_staff.cuenta)
                                stock_almacen = AlmacenStockModel.objects.filter(producto = producto_pedido.producto)
                           
                                lista_almacenes= []
                               
                                for almacen in almacenes:
                                    almacen_dic={'almacen':almacen,'cantidad_ingreso':0,'cantidad_egreso':0}
                                    lista_almacenes.append(almacen_dic)
                                
                          
                                for stock in stock_almacen:
   
                                    if stock.movimiento == 'INGRESO':
                                    
                                        for almacen in lista_almacenes:
                                        
                                            if stock.almacen == almacen['almacen']:
                                                almacen['cantidad_ingreso']+= stock.cantidad
                                                
                                    if stock.movimiento == 'EGRESO':
                                        
                                        for almacen in lista_almacenes:
                                            if stock.almacen == almacen['almacen']:
                                                almacen['cantidad_egreso']+= stock.cantidad 
                         
                                
                                for almacen in lista_almacenes:
                            
                                    cantidad_total= almacen['cantidad_ingreso'] - almacen['cantidad_egreso']
                                    
                                    if cantidad_pedido >0:
                                        if cantidad_pedido <= cantidad_total:
                                            
                                            AlmacenStockModel.objects.create(cantidad=cantidad_pedido,almacen= almacen['almacen'],producto=producto_pedido.producto,movimiento='EGRESO',nro_pedido=nuevo_pedido)
                                            cantidad_total -= cantidad_pedido
                                            cantidad_pedido=0
                                        else:
                                            AlmacenStockModel.objects.create(cantidad=cantidad_total,almacen= almacen['almacen'],producto=producto_pedido.producto,movimiento='EGRESO',nro_pedido=nuevo_pedido)
                                            cantidad_pedido -= cantidad_total


                                #CONTROLO STOCK PARA NOTICAR
                                control_stock_venta(producto=producto_pedido.producto)

                            else: 
                                #como no hay stock elimino el pedido y envio error
                                error= True
                                lista_prod_cantMax_para_error.append({'producto':producto_pedido.producto,'cantidad_maxima':producto_pedido.cantidad_venta})
                                
                        #controlo si algun producto dio error, elimino todo y preparo mensaje
                        if error:
                            detalle_eliminar= PedidoDetalleClienteModel.objects.filter(state=True, pedido=nuevo_pedido).all()
                            detalle_eliminar.delete()
                            nuevo_pedido.delete()
                            mensaje= 'Cantidad solicitada de los siguientes productos supera al stock en venta:\n'
                            for prod_error in lista_prod_cantMax_para_error:
                                mensaje+='{}, cantidad máxima:{}.\n'.format(prod_error['producto'],prod_error['cantidad_maxima'])


                        list_producto_detalle=[]

                        #armo el contexto para la respuesta
                        if not error:
                            detalle_pedido=PedidoDetalleClienteModel.objects.filter(state=True,pedido=nuevo_pedido)
                            notificacion_pedido_realizado(nuevo_pedido)


                            for producto in detalle_pedido:
                                list_producto_detalle.append(producto.json())
 

                            
                    except  :
                        error= True
                        mensaje=''
                        stock=AlmacenStockModel.objects.filter(producto= producto_pedido.producto)


                    context={
                        'error':error,
                        'mensaje':mensaje,
                        'data':{'pedido':[nuevo_pedido.json()],
                                'detalle_pedido':list_producto_detalle
                                }
                        }

                    return JsonResponse(context) 

                    
            else:
                return redirect('no_autorizado')    


      
        return redirect('pedidos')

       
class PedidoDetalleView(View):
    def get (self,request,pk,*args,**kwargs):
        HAS_ACCESS=False
        usuario = self.request.user
        
        if usuario.is_authenticated and usuario.is_active:
            if usuario.has_perm('distribuidora_app.view_pedidomodel'):

                HAS_ACCESS= True

                if pk != None:

                    pedidos_seleccionado=PedidoModel.objects.get(state=True,id= pk)
                    if pedidos_seleccionado.usuario.perfil.is_cliente:
                        detalle_pedido_seleccionado =PedidoDetalleClienteModel.objects.filter(state=True, pedido= pedidos_seleccionado)
                    else:    
                        detalle_pedido_seleccionado =PedidoDetalleModel.objects.filter(state=True, pedido= pedidos_seleccionado)

                    #si tengo permiso envio el form para editar el pedido
                    form_pedido_seleccionado=''
                    if usuario.has_perm('distribuidora_app.change_pedidomodel'):
                        form_pedido_seleccionado=PedidoCreateForm(instance=pedidos_seleccionado)
                    

                    '''lista_form_detalle=[]
                    for form_detalle in detalle_pedido_seleccionado:
                        lista_form_detalle.append(PedidoDetalleCreateForm(instance=form_detalle))'''
                    
                    context={
                        'usuario':usuario,
                        'HAS_ACCESS':HAS_ACCESS,
                        'pedido':pedidos_seleccionado,
                        'detalle_pedido':detalle_pedido_seleccionado,
                        'form_pedido':form_pedido_seleccionado,
                        #'form_detalle_pedido':lista_form_detalle
                    }

                    if usuario.has_perm('distribuidora_app.view_entregamodel'):

                        datos_entrega = EntregaModel.objects.get(id = pedidos_seleccionado.datos_entrega.id)
                        context['datos_entrega'] =datos_entrega

                else:
                    context={}
                

                return render(request,'app/pedidos/pedido_detalle.html',context )


        else:
            return redirect ('landing_home')
        
    def post(self,request,pk,*args,**kwargs):
        if request.user.is_authenticated and request.user.is_active:
            
            usuario= request.user
            
            if  usuario.is_staff and usuario.has_perm('distribuidora_app.change_pedidomodel') or usuario.perfil.is_proveedor:
             
                pedido= PedidoModel.objects.get(id=pk)
                estado_actual=pedido.estado#lo guardo ahora ya que luego al usar la instancia en el form, se modifica.
                form_pedido=PedidoEdicionForm(request.POST,instance=pedido)
                
                
                if form_pedido.is_valid():
                    
                    pedido_mod = form_pedido.save(commit=False)
                    
                    #cambio el estado
                    if cambio_estado_pedido(estado_actual,pedido):
                        
                        notificacion_cambio_estado(pedido, usuario_cambio=usuario)
                        
                    #Luego de verificar el estado guardo el cambio
                        pedido = form_pedido.save()

                return redirect('pedidos_detalle',pk)
           

            else:
                return redirect('no_autorizado')
        else:
            return redirect('landing_home')
                





# ============================================================== VISTAS STOCK ================================================================================


class StockView (View):
    def get (self,request,pk=None,*args,**kwargs):
        HAS_ACCESS=False
        usuario = self.request.user
        
        if usuario.is_authenticated and usuario.is_active:
            if usuario.has_perm('distribuidora_app.view_almacenstockmodel') and usuario.is_staff:
                HAS_ACCESS= True
                #traigo los almacenes
                almacenes=EntregaModel.objects.filter(state=True,cuenta=usuario.perfil.cuenta)

                if pk!=None:
                    almacen_seleccionado=EntregaModel.objects.get(id=pk)
                    stock_completo= AlmacenStockModel.objects.filter(state=True,almacen=almacen_seleccionado).all().order_by('-id')
                    totales_producto = cantidadPorProducto(almacen_seleccionado)
                else:    
                    stock_completo= AlmacenStockModel.objects.filter(state=True).all().order_by('-id')
                    totales_producto = cantidadPorProducto()
                
                
                context={
                    'HAS_ACCESS':HAS_ACCESS,
                    'list_stock':stock_completo,
                    'almacenList':almacenes,
                    'totales_producto':totales_producto
                    }


                return render(request,'app/stock/stock.html',context)
            return redirect('no_autorizado')
        return redirect('landing_home')


# ============================================================== PRODUCTOS EN VENTA  ================================================================================

class ProductosVentaView(View):
    def get (self,request,pk=None,*args,**kwargs):
        HAS_ACCESS=False
        usuario = self.request.user
        
        if usuario.is_authenticated and usuario.is_active:
            if usuario.has_perm('distribuidora_app.view_productoenventa') and usuario.is_staff:
                HAS_ACCESS=True


                #busco productos a la venta


                productos_en_venta=verificoCantidad_EnVenta(ProductoEnVenta.objects.filter(state=True).all().order_by('producto__id'))
                productos_en_almacenados=ProductosNOenVenta()
                

                context={
                        'HAS_ACCESS':HAS_ACCESS,
                        'productos_en_venta':productos_en_venta,
                        'productos_en_almacenados':productos_en_almacenados
            
                        }

                if pk != None:
                
                    if usuario.has_perm('distribuidora_app.change_productoenventa'):

                        producto_editable = ProductoAlmacenado.objects.filter(state=True,pk=pk).first()

                        
                        form_editable=ProductoEnVentaEditForm()
                        context['form_editable']=form_editable
                        context['producto_editable']=producto_editable.producto.id


                return render(request,'app/stock/productos_venta.html',context)
             #sin permisos   
            return redirect('no_autorizado')
        #no logueado
        return redirect('landing_home')

    
    def post (self,request,pk = None,*args,**kwargs):
        usuario = self.request.user
        HAS_ACCESS=False
        if usuario.is_authenticated and usuario.is_active:
            if usuario.has_perm('distribuidora_app.add_productoenventa') and usuario.is_staff:
                HAS_ACCESS=True
                producto_almacenado = ProductoAlmacenado.objects.filter(state=True,pk=pk).first()

                producto_enVenta = ProductoEnVentaEditForm(request.POST)

                if producto_enVenta.is_valid():
                    producto= ProductoEnVenta()
                    producto = producto_enVenta.save(commit=False)
                    producto.producto= producto_almacenado.producto
                    producto = producto_enVenta.save()
                
                return redirect('productos_venta')
            #sin permisos   
            return redirect('no_autorizado')
        #no logueado
        return redirect('landing_home')

               


def cambioEstadoProdVenta(request,pk):
    usuario= request.user
    if usuario.is_authenticated and usuario.is_active and usuario.is_staff:
        if usuario.has_perm('distribuidora_app.change_productoenventa'):
            
            producto_en_venta = ProductoEnVenta.objects.get(state=True,pk=pk)
            producto_en_venta.state =False
            producto_en_venta.save()
            return redirect('productos_venta')
        #sin permisos   
        return redirect('no_autorizado')
    #no logueado
    return redirect('landing_home')



# ============================================================================================================
#========================= PERFIL =====================


class PerfilView(View):
    def get(self,request,pk=None,*args,**kwargs):
        usuario = self.request.user
        HAS_ACCESS=False
        if usuario.is_authenticated:
            if usuario.has_perm('distribuidora_app.add_entregamodel'):
                HAS_ACCESS= True
                
                context ={
                    'HAS_ACCESS': HAS_ACCESS,
                    'domicilios': EntregaModel.objects.filter(cuenta=usuario.perfil.cuenta).all(),
                    'form_domicilios':EntregaCreateForm(),
                }


                if pk!=None:

                    context['form_edit_domicilio']=EntregaCreateForm(instance=EntregaModel.objects.get(id=pk))
                    context['docimilio_editable']=pk


                return render(request,'app/perfil/perfil.html',context)
            else:
                return redirect('no_autorizado')
        else:
            return redirect('landing')


    def post(self,request,pk=None,*args,**kwargs):
        usuario = self.request.user
        
        if usuario.is_authenticated:
            if usuario.has_perm('distribuidora_app.add_entregamodel'):
                
                if pk == None:
                    print('nuevo')
                    form= EntregaCreateForm(request.POST)

                    if form.is_valid():
                        domicilio= EntregaModel()
                        domicilio = form.save(commit=False)
                        domicilio.cuenta = usuario.perfil.cuenta
                        domicilio.save()
                else:
                    print('edit')
                    domicilio_editar=EntregaModel.objects.get(id=pk)
                    form= EntregaCreateForm(request.POST,instance=domicilio_editar)

                    if form.is_valid():
                        domicilio_editar = form.save()
                        

                return redirect('perfil')
            else:
                return redirect('no_autorizado')
        else:
            return redirect('landing')



#========================= INFORMES =====================


class InformesView(View):
    def get(self, request, *args, **kwargs):
        usuario = self.request.user
        HAS_ACCESS= False
        if usuario.is_authenticated:
            HAS_ACCESS= True
            if usuario.is_staff:
                agno= datetime.now().year
                mes= datetime.now().month
                ventas=PedidoModel.objects.filter(estado='ENTREGADO',usuario__perfil__is_cliente= True ,modified_date__year=agno,modified_date__month=mes).all()
                
                balance_list=[]
                resultado_periodo=0
                for pedido in ventas:
                    detalle_venta=PedidoDetalleClienteModel.objects.filter(pedido=pedido).all()
                    pedido_balance={'pedido': pedido,
                                    'productos':[],
                                    'total_ganancia':0
                                    }
                    total_ganancia=0
                    for producto in detalle_venta:
                        producto_bal={'nombre':producto.producto_venta.producto.name,
                        'costo':producto.producto_venta.producto.precio * producto.cantidad,
                        'precio_venta':producto.costo_total(),
                        'ganancia':producto.costo_total() - (producto.producto_venta.producto.precio * producto.cantidad)
                        }
                        pedido_balance['productos'].append(producto_bal)
                        total_ganancia+=producto_bal['ganancia']
                    pedido_balance['total_ganancia']=total_ganancia
                    resultado_periodo += pedido_balance['total_ganancia']
                    
                    balance_list.append(pedido_balance)


                context={
                    'HAS_ACCESS':HAS_ACCESS,
                    'balance_list': balance_list,
                    'resultado_periodo':resultado_periodo,
                    'periodo':'{}/{}'.format(mes,agno)
                }

                return render(request,'app/informes/informes.html',context)
            return redirect('no_autorizado')
        return redirect('landing')

    def post(self, request, *args, **kwargs):
        usuario= self.request.user
        HAS_ACCESS= False
        if usuario.is_authenticated:
            #if usuario.has_perm():
            if usuario.is_staff:
                HAS_ACCESS=True
                desde =request.POST.get('start')
                hasta =request.POST.get('end')

                ventas=PedidoModel.objects.filter(estado='ENTREGADO',usuario__perfil__is_cliente= True ,modified_date__gte=desde, modified_date__lte=hasta ).all()
                
                balance_list=[]
                resultado_periodo=0
                for pedido in ventas:
                    detalle_venta=PedidoDetalleClienteModel.objects.filter(pedido=pedido).all()
                    pedido_balance={'pedido': pedido,
                                    'productos':[],
                                    'total_ganancia':0
                                    }
                    total_ganancia=0
                    for producto in detalle_venta:
                        producto_bal={'nombre':producto.producto_venta.producto.name,
                        'costo':producto.producto_venta.producto.precio * producto.cantidad,
                        'precio_venta':producto.costo_total(),
                        'ganancia':producto.costo_total() - (producto.producto_venta.producto.precio * producto.cantidad)
                        }
                        pedido_balance['productos'].append(producto_bal)
                        total_ganancia+=producto_bal['ganancia']
                    pedido_balance['total_ganancia']=total_ganancia
                    resultado_periodo += pedido_balance['total_ganancia']
                    
                    balance_list.append(pedido_balance)


                context={
                    'HAS_ACCESS':HAS_ACCESS,
                    'balance_list': balance_list,
                    'resultado_periodo':resultado_periodo,
                    'periodo': '{} | {}'.format(desde,hasta),
                    'desde': desde,
                    'hasta':hasta
                }

                return render(request,'app/informes/informes.html',context)


            return redirect ('no_autorizado')
        return redirect('landing')