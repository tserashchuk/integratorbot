from celery import shared_task
import requests
from datetime import date, datetime, timedelta
from tgusers.models import Client
from openai import OpenAI

@shared_task
def addf(user):
   myuser = Client.objects.get(tgid=user)
   myuser_hook = myuser.clientuser.first
   requests.get('https://api.telegram.org/bot8136233806:AAGkSfMW81OkcKffxwcFuZVZul7-_n81My8/sendMessage?chat_id='+user+'&text='+str(myuser_hook.url))


   client = OpenAI(api_key="sk-84f8be873ef144618d50838c7b548fcd", base_url="https://api.deepseek.com")

   response = client.chat.completions.create(
      model="deepseek-chat",
      messages=[
         {"role": "system", "content": "You are a helpful assistant"},
         {"role": "user", "content": "Hello"},
      ],
      stream=False
   )
   requests.get('https://api.telegram.org/bot8136233806:AAGkSfMW81OkcKffxwcFuZVZul7-_n81My8/sendMessage?chat_id='+user+'&text='+str(print(response.choices[0].message.content)))
   return 'f'