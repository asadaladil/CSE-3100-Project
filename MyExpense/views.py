from django.shortcuts import render
from accounts.models import *
from accounts.constants import *


def note(id):
    return (UserRegisterModel.objects.get(user_id=id).notify[0][0])


def homepage(request):
    if request.user.is_authenticated: 
        return render(request,'home.html',{'notify':note(request.user.id)})
    return render(request,'home.html')

