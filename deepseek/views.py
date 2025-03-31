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

class AddHook(LoginRequiredMixin,View):

    login_url = '/login'
    
    def get(self,request):
        current_user = request.user
        current_user = Client.objects.get(djuser=current_user)

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        options = Options()
        options.add_argument("start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://www.google.com")
        return render(request,'addhook.html')
    
    def post(self,request):
        current_user = request.user
        current_user = Client.objects.get(djuser=current_user)
        value = request.POST.get("cre", "")
        if value == '1':
            ou = PeriodicTask.objects.create(crontab=CrontabSchedule.objects.get(id=2), name='Формула прибыли каждый день '+str(current_user.tgid), task='deepseek.tasks.addf',kwargs=json.dumps({'user': str(current_user.tgid)}))
            current_user.tasks.add(ou)
        elif value == '2':
            print("You're yet to be born")
        else: 
            print("You're yet to be born")
        return redirect('cabinet')