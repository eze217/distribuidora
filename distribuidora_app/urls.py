from django.contrib import admin
from django.urls import path

from .views import home,Home_App,ProveedoresView,ProveedorDetalleView,proveedorEliminaView,prohibido
from .views import ProductosView,productoEliminaView



from .views import PedidosView,PedidoCreateView,PedidosJsonView,PedidoDetalleView


urlpatterns = [
    path('', home, name='landing_home'),
    path('home/',Home_App.as_view(),name='home-app'),
    path('proveedores/',ProveedoresView.as_view(),name='proveedores'),
    path('proveedores/<int:pk>',ProveedorDetalleView.as_view(),name='proveedor_detalle'),
    path('proveedores_delete/<int:pk>',proveedorEliminaView,name='proveedor_elimina'),

    path('productos/',ProductosView.as_view(),name='productos'),
    path('producto_edit/<int:pk>',ProductosView.as_view(),name='producto_edita'),
    path('producto_delete/<int:pk>',productoEliminaView,name='producto_elimina'),

    path('pedidos/',PedidosView.as_view(),name='pedidos'),
    path('pedidos/<int:pk>',PedidoDetalleView.as_view(),name='pedidos_detalle'),
    path('pedidos_create/',PedidoCreateView.as_view(),name='pedido_create'),
    path('pedidos_proveedor/',PedidosJsonView.as_view(),name='pedidos_rest_sipk'),
    path('pedidos_proveedor/<int:pk>',PedidosJsonView.as_view(),name='pedidos_rest'),
    #path('cambio_estado_pedido/<estado>/<int:pk>',cambio_estado_pedido,name='cambio_estado_pedido'),
    


    path('prohibido/',prohibido,name='no_autorizado')
]
