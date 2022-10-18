from django.shortcuts import render,redirect
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


def marcar_leida(request,pk):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if request.user.has_perm('notificacion.change_notificacionmodel'):
                notificacion = NotificacionModel.objects.get(id=pk)
                notificacion.leida= True
                notificacion.save()
                return redirect('home-app')
            else:
                return redirect('no_autorizado')
    else:
        return redirect ('landing_home')

def borrar_notificacion(request,pk):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if request.user.has_perm('notificacion.delete_notificacionmodel'):
                notificacion = NotificacionModel.objects.get(id=pk)
                notificacion.state= False
                notificacion.save()
                return redirect('home-app-leida','leidas')
            else:
                return redirect('no_autorizado')
    else:
        return redirect ('landing_home')

               
        
            