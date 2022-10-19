
from django.urls import path

from user.views import ControlLogin,logout_user,NuevoUserView,creacion_cuenta

urlpatterns = [
    path('', ControlLogin.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registro/',NuevoUserView.as_view(),name='registro'),
    path('fin_registro/',creacion_cuenta,name='fin_registro'),
    
   
]
