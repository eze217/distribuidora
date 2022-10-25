
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.models import User,Group
from django.contrib.auth import login, authenticate,logout

from distribuidora_app.models import CuentaModel
from .models import Perfil
from .forms import UserForm
from distribuidora_app.forms import ProveedorForm


# Create your views here.

class ControlLogin(View):

    def get (self,request,*args,**kwargs):
        
        if  not self.request.user.is_authenticated: 
                  
            return render(request,'login.html',{})

        else:
            return redirect('home-app')
    
    def post(self,request,*arg,**kwargs):
        if  not self.request.user.is_authenticated:
            user_name=request.POST['user_name']
            user_pass=request.POST['user_pass']
            
            context={}
            
            try:
                user = User.objects.get(username=user_name)
            except:
                context['mensaje']='Usuario inexistente'    
                return render(request,'login.html',context)

            
            if user.is_active:
                if user is not None and user.check_password(user_pass):
                    perfil= Perfil.objects.filter(usuario=user).first()
                   
                    if perfil!= None:
                        usuario= authenticate(username=user_name,password=user_pass)
                        login(self.request,usuario)
                        if perfil.cuenta != None :
                            return redirect('home-app')
                        else:
                            #continua registro
                            context={'form':ProveedorForm()}

                            return render(request,'registro.html',context)
                            
                    else:
                        context['mensaje']='El usuario NO posee cuenta asociada. Ver con el administrador'
                        
                else:
                    context['mensaje']='Usuario y/o contraseña erroneo'

                return render(request,'login.html',context)
            else:
                context['mensaje']='Usuario inactivo'

                return render(request,'login.html',context)
            
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('landing_home')          


#Creación user nuevo.

class NuevoUserView(View):
    def get ( self, request,pk=None , *args, **kwargs):
        #este registro es solo para clientes

        form= UserForm()
       
        context={
            'form':form,
        }

        
        return render(request,'new_user_cliente.html',context)
    
    def post(self, request,pk =None , *args, **kwargs):

        
        form= UserForm(request.POST)
        
        if form.is_valid():
            user_cliente= User()
            user_cliente=form.save()
            if pk != None:
                if self.request.user.has_perm('auth.add_user'):
                    group = Group.objects.get(name='proveedor')
                    user_cliente.groups.add(group)
                    cuenta_proveedor = CuentaModel.objects.get(id = pk)
                    Perfil.objects.create(usuario=user_cliente,is_proveedor=True,is_cliente=False,cuenta = cuenta_proveedor)
                    return redirect('proveedor_detalle',pk)
                return redirect('no_autorizado')
            else:
                group = Group.objects.get(name='cliente')
                user_cliente.groups.add(group)
                Perfil.objects.create(usuario=user_cliente,is_proveedor=False,is_cliente=True)
               
        return redirect('home-app')


#creacion cuenta

def creacion_cuenta(request):
    usuario= request.user
    if request.method == 'POST':
        if usuario.is_authenticated:
            form = ProveedorForm(request.POST)
            if form.is_valid():
                cuenta =CuentaModel()
                cuenta = form.save()
                perfil=Perfil.objects.get(usuario=usuario)
                perfil.cuenta= cuenta
                perfil.save()
                return redirect('home-app')
    else:
        return redirect('no_autorizado')



#en el control login verificar que el usuario tenga perfil asociado, caso contrario redirigir a la pantalla de configuraciones(deberia ser una sin navbar)