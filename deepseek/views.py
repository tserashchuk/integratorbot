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

from selenium import webdriver

class AddHook(LoginRequiredMixin,View):

    login_url = '/login'
    
    def get(self,request):
        current_user = request.user
        current_user = Client.objects.get(djuser=current_user)

        return render(request,'addhook.html')
    
    def post(self,request):
        current_user = request.user
        current_user = Client.objects.get(djuser=current_user)
        value = request.POST.get("cre", "")
        if value == '1':
            ou = PeriodicTask.objects.create(crontab=CrontabSchedule.objects.get(id=2), name='ТОП3 сделок за неделю '+str(current_user.tgid), task='deepseek.tasks.addf',kwargs=json.dumps({'user': str(current_user.tgid)}))
            current_user.tasks.add(ou)
        elif value == '2':
            ou = PeriodicTask.objects.create(crontab=CrontabSchedule.objects.get(id=2), name='Менеджеры и сделки '+str(current_user.tgid), task='deepseek.tasks.reccomend_event',kwargs=json.dumps({"user": str(current_user.tgid),"prompt":"добавь к ответу краткую рекомендацию в одном абзаце о заполнении данных в битрикс24 если данные заполнены не полностью. если они заполнены хорошо то дополни ответ одним коротким абзацем в котором приведи о пример из мировых практик работы с отделом продаж. в результате пришли мне выводы из моего первого сообщения и одну из этих рекомендаций. Не используй символ * для форматирования"}))
            current_user.tasks.add(ou)
        elif value == '3':
            ou = PeriodicTask.objects.create(crontab=CrontabSchedule.objects.get(id=2), name='Менеджеры и сделки '+str(current_user.tgid), task='deepseek.tasks.reccomend',kwargs=json.dumps({"user": str(current_user.tgid),"prompt":str(current_user.about)}))
            current_user.tasks.add(ou)
        else: 
            print("You're yet to be born")
        return redirect('cabinet')