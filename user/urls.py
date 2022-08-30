
from django.urls import path

from user.views import ControlLogin,logout_user

urlpatterns = [
    path('', ControlLogin.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
   
]
