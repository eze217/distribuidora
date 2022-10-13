from django.urls import path

from .views import NotificacionesJsonItemView

urlpatterns = [
    path('count/', NotificacionesJsonItemView.as_view(), name='notificaciones_count'),
    
]

