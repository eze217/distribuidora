from django.urls import path

from .views import NotificacionesJsonItemView,marcar_leida,borrar_notificacion

urlpatterns = [
    path('count/', NotificacionesJsonItemView.as_view(), name='notificaciones_count'),
    path('leida/<int:pk>', marcar_leida, name='marcar_leida'),
    path('delete/<int:pk>', borrar_notificacion, name='borrar_notificacion'),
    
]

