from django.shortcuts import render,redirect
from django.contrib.auth import logout
from accounts.models import *
from accounts.forms import PasswordChangeForm
from django.contrib import messages
from accounts.constants import *
from django.conf import settings
import os


def note(id):
    acc=UserRegisterModel.objects.get(user_id=id)
    notify=acc.notify[0][0]
    pic=acc.photo
    return [notify,pic]

def homepage(request):
    if request.user.is_authenticated: 
        return render(request,'home.html',{'notify':note(request.user.id)[0],'pic':note(request.user.id)[1]})
    return render(request,'home.html')

def Change_Password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            acc=UserRegisterModel.objects.get(user_id=request.user.id)
            pass1=request.POST.get('pass1')
            a=acc.user.check_password(pass1)
            pass2=request.POST.get('pass2')
            pass3=request.POST.get('pass3')
            if pass1==pass2 and pass2==pass3:
                messages.error(request,"Old and New Password must be different!!")
                return redirect('/password/')
            if acc.user.check_password(pass1)==False:
                messages.error(request,"Old Password is incorrect!!")
                return redirect('/password/')
            if pass2!=pass3:
                messages.error(request,"New Password and Confirm Password must be same!!")
                return redirect('/password/')
            acc.user.set_password(pass2)
            acc.user.save()
            messages.success(request,"Password Changed Successfully!!")
            messages.success(request,"You are SIGNED OUT. Enter Again? Then go to SIGN IN PAGE !!")
            return redirect('/')
        form=PasswordChangeForm()
        acc=UserRegisterModel.objects.get(user_id=request.user.id)
        return render(request,'password.html',{'forms':form,'notify':note(request.user.id)[0],
                                               'pic':note(request.user.id)[1]})

def Delete_Page(request):
    if request.user.is_authenticated:
        return render(request,"delete.html",{'notify':note(request.user.id)[0],'pic':note(request.user.id)[1]})
    return render(request,"page404.html")

def Delete(request):
    if request.user.is_authenticated:
        acc=UserRegisterModel.objects.get(user_id=request.user.id)
        file_path=str(acc.photo)
        if file_path:
            full_path=os.path.join(settings.MEDIA_ROOT, file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        logout(request)
        acc.user.delete()  
        messages.success(request,"Account is Deleted Successfully!")
        return redirect('/') 
    else:
        return render(request,"page404.html") 

def otp(request):
    if request.user.is_authenticated:
        messages.success(request,"")
        return redirect('/accounts/dashboard/')