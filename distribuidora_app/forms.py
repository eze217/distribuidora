from dataclasses import fields
from django.forms import forms,ModelForm
from distribuidora_app.models import CuentaModel,ProductoModel,PedidoModel,PedidoDetalleModel

# ============================ PROVEEDOR  ============================
class ProveedorForm(ModelForm):
    class Meta:
        model=CuentaModel
        fields='__all__'
        exclude=['state']
        
# ============================ PRODUCTO  ============================

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

# ============================ PEDIDOS  ============================

class PedidoCreateForm(ModelForm):
    class Meta:
        model= PedidoModel
        fields='__all__'
        

class PedidoDetalleCreateForm(ModelForm):
    class Meta:
        model= PedidoDetalleModel
        fields='__all__'
        exclude= ['state','pedido']

class PedidoEdicionForm(ModelForm):
    class Meta:
        model= PedidoModel
        fields=['estado']
        
