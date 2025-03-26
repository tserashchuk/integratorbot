from celery import shared_task
import requests
from datetime import date, datetime, timedelta
from tgusers.models import Client

@shared_task
def addf(user):
   print(user)
   requests.get('https://api.telegram.org/bot8136233806:AAGkSfMW81OkcKffxwcFuZVZul7-_n81My8/sendMessage?chat_id='+user+'&text=helliend')
   return 'f'