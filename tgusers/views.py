from django.shortcuts import render

import requests
import json
from tgusers.models import *
from bitrix24 import *
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from bitrix24 import *
from openai import OpenAI
# Create your views here.
class Cabinet(LoginRequiredMixin,View):

    login_url = '/login'
    
    def get(self,request):
        current_user = request.user
        current_user = Client.objects.get(djuser=current_user)
        return render(request,'cabinet.html',{'current_user':current_user})
    

    

class Register(View):
    def get(self,request):
        current_user = request.user
        if current_user is not None:
            if current_user.is_active:               
                return redirect('cabinet')
        return render (request, 'register.html')

    def post(self,request):
        name = request.POST.get("name", "")
        password = request.POST.get("password", "")
        chatid = request.POST.get("chatid", "")
        tusername = request.POST.get("tusername", "")
        formhook = request.POST.get("hook", "")
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('cabinet')
        else:
            user = User.objects.create_user(username=name, password=password)
            hook = ClientHook.objects.create(hook=formhook,name=str(user.username)+' deals')
            myuser = Client.objects.create(djuser=user, tgname=tusername, tgid=chatid, clientuser=hook)
            login(request, user)
            return redirect('cabinet')
    

    
class Login(View):
    def get(self,request):
        current_user = request.user
        if current_user is not None:
            if current_user.is_active:               
                return redirect('cabinet')
        return render (request, 'login.html')

    def post(self,request):
        name = request.POST.get("name", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('cabinet')
        else:
            return redirect('login')

        
        
class Logout(View):
    def get(self,request):
        current_user = request.user
        if current_user:
            logout(request) 
        return redirect('login')   


