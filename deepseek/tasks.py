from celery import shared_task
import requests
from datetime import date, datetime, timedelta
from tgusers.models import Client

@shared_task
def addf(user):
   myuser = Client.objects.get(tgid=user)
   myuser_hook = myuser.clientuser['0']
   requests.get('https://api.telegram.org/bot8136233806:AAGkSfMW81OkcKffxwcFuZVZul7-_n81My8/sendMessage?chat_id='+user+'&text='+str(myuser.clientuser['0']))
   return 'f'