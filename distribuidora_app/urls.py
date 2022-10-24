from typing import List
from django.contrib import admin
from django.urls import path

from .views import home,Home_App,ProveedoresView,ProveedorDetalleView,proveedorEliminaView,prohibido
from .views import ProductosView,productoEliminaView



from .views import PedidosView,PedidoCreateView,PedidosJsonView,PedidoDetalleView,StockView,ProductosVentaView,cambioEstadoProdVenta

from .views import PerfilView


urlpatterns = [
    path('', home, name='landing_home'),
    path('home/',Home_App.as_view(),name='home-app'),
    path('home/<str:leidas>',Home_App.as_view(),name='home-app-leida'),
    

    path('proveedores/',ProveedoresView.as_view(),name='proveedores'),
    path('proveedores/<int:pk>',ProveedorDetalleView.as_view(),name='proveedor_detalle'),
    path('proveedores_delete/<int:pk>',proveedorEliminaView,name='proveedor_elimina'),

    path('productos/',ProductosView.as_view(),name='productos'),
    path('producto_edit/<int:pk>',ProductosView.as_view(),name='producto_edita'),
    path('producto_delete/<int:pk>',productoEliminaView,name='producto_elimina'),

    path('pedidos/',PedidosView.as_view(),name='pedidos'),
    path('pedidos/<int:pk>',PedidoDetalleView.as_view(),name='pedidos_detalle'),
    path('pedidos_create/',PedidoCreateView.as_view(),name='pedido_create'),
    path('pedidos_create/<int:pk>',PedidoCreateView.as_view(),name='pedido_create_pk'),
    path('pedidos_proveedor/',PedidosJsonView.as_view(),name='pedidos_rest_sipk'),
    path('pedidos_proveedor/<int:pk>',PedidosJsonView.as_view(),name='pedidos_rest'),
    #path('cambio_estado_pedido/<estado>/<int:pk>',cambio_estado_pedido,name='cambio_estado_pedido'),
    
    path('stock/',StockView.as_view(),name='stock'),
    path('stock/<int:pk>',StockView.as_view(),name='stock_almacen'),

    path('productos_venta/',ProductosVentaView.as_view(),name='productos_venta'),
    path('productos_venta/<int:pk>',ProductosVentaView.as_view(),name='productos_venta_edit'),
    path('productos_venta_cancel/<int:pk>',cambioEstadoProdVenta,name='productos_venta_cancel'),

    path('perfil/',PerfilView.as_view(),name='perfil'),




    path('prohibido/',prohibido,name='no_autorizado')
]




