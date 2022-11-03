
from django.urls import path

from user.views import ControlLogin,logout_user,NuevoUserView,creacion_cuenta,registro_plataforma

urlpatterns = [
    path('', ControlLogin.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registro/',NuevoUserView.as_view(),name='registro'),
    path('registro/proveedor/<int:pk>',NuevoUserView.as_view(),name='user_proveedor'),
    path('fin_registro/',creacion_cuenta,name='fin_registro'),
    path('registro/primer-ingreso',registro_plataforma,name='registro_plataforma'),

    
   
]
