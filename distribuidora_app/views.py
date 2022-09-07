
from django.shortcuts import render,redirect
from django.views import View
from django.http.response import JsonResponse
from distribuidora_app.forms import ProveedorForm,ProductoAdminForm,ProductoForm,ProductoEditForm
from distribuidora_app.forms import PedidoDetalleCreateForm,PedidoCreateForm
from distribuidora_app.forms import PedidoEdicionForm

from distribuidora_app.models import PedidoDetalleModel, PedidoModel, CuentaModel,ProductoModel,EntregaModel

from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test



import json
from django.core.serializers.json import DjangoJSONEncoder

from user.models import Perfil


'''
# Create your views here.
def group_required(*group_names):
    """ Grupos, checar si pertenece a grupo """
    print('entre',group_names)
    def check(user):
        print('user',user)
        if user.groups.filter(name__in=group_names).exists() | user.is_superuser:
            return True
        else:
            return False
    return user_passes_test(check, login_url='/prohibido/')
'''


#@group_required('distribuidores','proveedores') 
def home (request):
    
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home-app')
        return render(request,'landing/index.html',{})


def prohibido(request):
    if request.user.is_authenticated:
        context={
            'HAS_ACCESS':True
        }
        return render(request,'core_template/no_autorizado.html',context)

    


class Home_App(View):
   
    
    def get(self,request,*args,**kwargs):
        HAS_ACCESS=False
        context= {}  
        if self.request.user.is_authenticated:
            HAS_ACCESS=True
        
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


                #proveedoresList= CuentaModel.objects.filter(state=True).all()
  
                #buscar los proveedores que son solo proveedores
                proveedoresPerfil=Perfil.objects.filter(is_proveedor=True).all()
                
                proveedoresList=[]
                for pp in proveedoresPerfil:
                    if pp.is_proveedor:
                        
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

            #if str(usuario.groups.get())=='distribuidora':  
               
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


                

                #======================== IMPORTANTE FALTA RESPUESTAS PARA CLIENTES =================
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
               

                        #proveedoresList= CuentaModel.objects.filter(state=True)#envio listado de proveedores para seleccionar
                        context['proveedoresList']=proveedoresList
                    #busco mis almacenes
                    entrega=EntregaModel.objects.filter(state=True,cuenta=usuario.perfil.cuenta)
                    context['entrega']=entrega

                elif usuario.perfil.is_cliente:#valido sea cliente, proveedores NO hacen pedidos
                    # ================= ATENCION =======================0
                    #Acá debo buscar los productos que tengo en stock, NO desde la tabla productos
                    productosList=ProductoModel.objects.filter(state=True)
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
                            
                    print(' Hace pedido el cliente ')
                    error=True

                    '''
                    En cliente debo tomar los productos para los pedidos desde los productos que tengo en almacen
                    pero a tener en cuenta los costos, debo crear una clase donde los costos de compra sean diferente 
                    al  precio de venta
                    
                    '''

                    context={
                        'error':error,
                        'data':{'pedido':'[nuevo_pedido.json()]',
                                'detalle_pedido':'list_producto_detalle'
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
                    detalle_pedido_seleccionado =PedidoDetalleModel.objects.filter(state=True, pedido= pedidos_seleccionado)
                    #if usuario.is_staff : 
                        #Traigo el pedido y el detalle y el FORM para ver y editar

                    form_pedido_seleccionado=PedidoCreateForm(instance=pedidos_seleccionado)
                    
                    lista_form_detalle=[]
                    for form_detalle in detalle_pedido_seleccionado:
                        lista_form_detalle.append(PedidoDetalleCreateForm(instance=form_detalle))
                    '''
                    elif usuario.perfil.is_proveedor: 
                        
                        pedidos_list=PedidoModel.objects.filter(state=True,proveedor=usuario.perfil.cuenta).order_by('-id')
                    elif usuario.perfil.is_cliente:
                        pedidos_list=PedidoModel.objects.filter(state=True,usuario=usuario).order_by('-id')'''
                    
                    
                    context={
                        'usuario':usuario,
                        'HAS_ACCESS':HAS_ACCESS,
                        'pedido':pedidos_seleccionado,
                        'detalle_pedido':detalle_pedido_seleccionado,
                        'form_pedido':form_pedido_seleccionado,
                        'form_detalle_pedido':lista_form_detalle
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
                
                form_pedido=PedidoEdicionForm(request.POST,instance=pedido)
                
                if form_pedido.is_valid():
                    pedido = form_pedido.save()
                

                return redirect('pedidos_detalle',pk)
           

            else:
                return redirect('no_autorizado')
        else:
            return redirect('landing_home')
                



'''
def cambio_estado_pedido(request,estado,pk):
    
    if request.method == 'GET':
        
        if request.user.is_authenticated and request.user.is_active:
            
            usuario= request.user
            
            if  usuario.is_staff and usuario.has_perm('distribuidora_app.change_pedidomodel'):
             
                nuevo_estado=estado      
                pedido= PedidoModel.objects.get(id=pk)
               
                form_pedido=PedidoCreateForm(estado=nuevo_estado,instance=pedido)
                print(form_pedido.is_valid())
                if form_pedido.is_valid():
                    print('ok')
                    pedido= form_pedido.save(commit=False)
                    pedido.estado=nuevo_estado
                    pedido = form_pedido.save()

                    return JsonResponse({'ok':True})
    
    return JsonResponse({'ok':True})'''

