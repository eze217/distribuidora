
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout



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
                    print(user_name,user_pass,user)
                    usuario= authenticate(username=user_name,password=user_pass)
                    login(self.request,usuario)
                    return redirect('home-app')
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