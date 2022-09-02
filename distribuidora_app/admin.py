from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(CuentaModel)
admin.site.register(ProductoModel)
admin.site.register(PedidoModel)
admin.site.register(PedidoDetalleModel)
admin.site.register(AlmacenModel)
admin.site.register(AlmacenStockModel)

