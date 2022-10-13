from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse

from .models import NotificacionModel

# Create your views here.


class NotificacionesJsonItemView(View):

    def get(self,request,*args,**kwargs):
        usuario= self.request.user
        HAS_ACCESS=False
      
        if usuario.is_authenticated:
            if usuario.has_perm('notificacion.view_notificacionmodel'):
                notificaciones= NotificacionModel.objects.filter(state=True,cuenta_notificada=usuario.perfil.cuenta,leida=False).all().count()
                
                data= {
                    'error': False,
                    'data':notificaciones
                }
                return JsonResponse (data)
               
        
            