from dataclasses import fields
from django.forms import forms,ModelForm
from distribuidora_app.models import ProveedorModel,ProductoModel,PedidoModel,PedidoDetalleModel

class ProveedorForm(ModelForm):
    class Meta:
        model=ProveedorModel
        fields='__all__'
        exclude=['state']
        

class ProductoAdminForm(ModelForm):
    class Meta:
        model=ProductoModel
        fields='__all__'
        exclude=['state']


class ProductoForm(ModelForm):
    class Meta:
        model=ProductoModel
        fields='__all__'
        exclude=['state','proveedor','almacen']


class ProductoEditForm(ModelForm):
    class Meta:
        model=ProductoModel
        fields=['name','descripcion','proveedor']


class PedidoCreateForm(ModelForm):
    class Meta:
        model= PedidoModel
        fields='__all__'
        

class PedidoDetalleCreateForm(ModelForm):
    class Meta:
        model= PedidoDetalleModel
        fields='__all__'
        exclude= ['state','pedido']