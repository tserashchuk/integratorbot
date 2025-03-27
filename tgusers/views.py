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

        myuser = Client.objects.get(tgid='553875205')
        myuser_hook = myuser.clientuser.all()
        # requests.get('https://api.telegram.org/bot8136233806:AAGkSfMW81OkcKffxwcFuZVZul7-_n81My8/sendMessage?chat_id=553875205&text='+str(myuser_hook[0].url))


        bx24 = Bitrix24(str(myuser_hook[0].url))
        data = bx24.callMethod('crm.deal.list',
                       filter={'CLOSED': 'N',
                               '>DATE_MODIFY':'2025-01-01'},)

        client = OpenAI(api_key="sk-84f8be873ef144618d50838c7b548fcd", base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": 'пока ничего не делай с этими данными '+str(data)},
                {"role": "user", "content": "выдели самые важные сделки с точки зрения максимизации прибыли, ответь кратко текстом без сложного форматирования"},
            ],
            stream=False
        )
        requests.get('https://api.telegram.org/bot8136233806:AAGkSfMW81OkcKffxwcFuZVZul7-_n81My8/sendMessage?chat_id=553875205&text='+str(response.choices[0].message.content))
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


