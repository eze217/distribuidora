
from django.db import models

from django.conf import settings
from django.contrib.auth.models import User





# Create your models here.

class BasicModel(models.Model):
    id=models.AutoField(primary_key= True)
    state = models.BooleanField('Estado', default=True)
    created_date= models.DateField('Fecha de creación',auto_now=False, auto_now_add=True)
    modified_date= models.DateField('Fecha de modificación',auto_now=True, auto_now_add=False)
    deleted_date= models.DateField('Fecha de eliminación',auto_now=True, auto_now_add=False)
    
    class Meta:
        abstract = True
        verbose_name='Modelo Base'
        verbose_name_plural='Modelos Base'

class AlmacenModel( BasicModel):
    name= models.CharField(verbose_name='Nombre',max_length=100,blank=False,null=False)
    address= models.CharField(verbose_name='Domicilio',max_length=200,blank=False,null=False)
    phone=models.CharField(verbose_name='Telefono',max_length=15,blank=False,null=False)

    class Meta:
        verbose_name='Almacen'
        verbose_name_plural='Almacenes'
    
    def __str__(self):
        return self.name


class Cuenta(BasicModel):
    name= models.CharField(verbose_name='Nombre',max_length=100,blank=False,null=False)
    domicilio= models.CharField(verbose_name='Domicilio',max_length=200,blank=False,null=False)
    telefono= models.CharField(verbose_name='Telefono',max_length=15,blank=False,null=False)
    cif= models.CharField(verbose_name='CIF',max_length=20,blank=False,null=False)
    observaciones=models.CharField(verbose_name='Notas',max_length=200,blank=True,null=True,default='---')

    class Meta:
        verbose_name= 'Proveedor'
        verbose_name_plural='Proveedores'
    
    def __str__(self):
        return self.name

    
class ProductoModel(BasicModel):
    name= models.CharField(verbose_name='Nombre producto',max_length=100,blank=False,null=False)
    precio= models.FloatField(blank=False,null=False)
    descripcion= models.CharField(verbose_name='Descripción',max_length=200)
    
    
    proveedor = models.ForeignKey(ProveedorModel,on_delete=models.CASCADE)

    class Meta:
        verbose_name= 'Producto'
        verbose_name_plural='Productos'
    
    def __str__(self):
        return self.name


    def json(self):
        data={ 'id':self.id,
        'name':self.name,
        'precio':self.precio,
        'descripcion':self.descripcion
        }
        return data
    
class AlmacenStockModel(BasicModel):
    cantidad=models.IntegerField()
    producto= models.ForeignKey(ProductoModel, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('INGRESO', 'INGRESO'),
        ('EGRESO', 'EGRESO')
        )
    movimiento=models.CharField(verbose_name='Movimiento',choices=TYPE_CHOICES,max_length=10)
    
    
    class Meta:
        verbose_name= 'Almacen Stock'
        verbose_name_plural='Almacen Stock'
    
    def __str__(self):
        return self.cantidad,self.producto,self.movimiento




class PedidoModel (BasicModel):
    TYPE_CHOICES = (
        ('SOLICITADO', 'SOLICITADO'),
        ('CONFIRMADO', 'CONFIRMADO'),
        ('EN PREPARACION', 'EN PREPARACION'),
        ('ANULADO', 'ANULADO'),
        ('EN REPARTO', 'EN REPARTO'),
        ('ENTREGADO', 'ENTREGADO')
    )

    estado = models.CharField(verbose_name='Estado ', choices=TYPE_CHOICES, max_length=20)
    proveedor = models.ForeignKey(ProveedorModel,on_delete=models.CASCADE)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    TYPE_PEDIDO=(('COMPRA','COMPRA'),('VENTA','VENTA'))
    tipo_pedido= models.CharField(verbose_name='Tipo de pedido',choices=TYPE_PEDIDO,max_length=10)

    class Meta:
        verbose_name='Pedido'
        verbose_name_plural= 'Pedidos'
    
    def __str__(self):
        return str(self.id)

    def json(self):
        data={
            'id':self.id,
            'estado':self.estado,
            'proveedor':self.proveedor.name,
            'usuario':self.usuario.username,
            'tipo_pedido':self.tipo_pedido

        }
        return data
    

class PedidoDetalleModel (BasicModel):
    
    pedido = models.ForeignKey(PedidoModel, on_delete=models.CASCADE)
    cantidad=models.IntegerField()
    producto= models.ForeignKey(ProductoModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name='Pedido detalle'
        verbose_name_plural= 'Pedidos detalle'
    
    def __str__(self):
        return str(self.pedido.id)

    def costo_total(self):
        return  self.producto.precio * self.cantidad 

    def json(self):
        data={
            'proveedor':self.pedido.id,
            'cantidad':self.cantidad,
            'producto':self.producto.name,
            'precio_unitario':self.producto.precio,
            'costo':self.costo_total(),
            

        }
        return data

    

