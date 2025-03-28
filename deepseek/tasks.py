from celery import shared_task
import requests
from datetime import date, datetime, timedelta
from tgusers.models import Client
from openai import OpenAI
from bitrix24 import *

@shared_task
def addf(user):
   myuser = Client.objects.get(tgid=user)
   myuser_hook = myuser.clientuser.all()
   # requests.get('https://api.telegram.org/bot8136233806:AAGkSfMW81OkcKffxwcFuZVZul7-_n81My8/sendMessage?chat_id=553875205&text='+str(myuser_hook[0].url))


   bx24 = Bitrix24(str(myuser_hook[0].url))
  
   data = bx24.callMethod('crm.deal.list',
                  filter={'CLOSED': 'N',
                           '>DATE_CREATE':'2025-03-23'},
                  select=['ID', 'TITLE', 'STAGE_ID','DATE_CREATE','DATE_MODIFY','CREATED_BY_ID','ASSIGNED_BY_ID','OPPORTUNITY','IS_RETURN_CUSTOMER','CONTACT_ID'])
   

   client = OpenAI(api_key="sk-84f8be873ef144618d50838c7b548fcd", base_url="https://api.deepseek.com")
   messages=[
            {"role": "system", "content": 'представь что ты бизнес-аналитик. это json из crm системы битрикс24, '+str(data)},
            {"role": "user", "content": 'систематизируй эти данные'}
      ]
   response = client.chat.completions.create(
      model="deepseek-reasoner",
      messages=messages
   )
   messages.append(response.choices[0].message.content)
   messages.append({"role": "user", "content": "выдели самые прибыльные сделки и напиши кому из лучше обработать. подготовь ответ на вопрос пользователя таким образом чтобы он был кратким и его можно было его отправить в телеграм - для выделения курсива и жирного шрифта используй html теги. Обрати внимание что название сделок хранится в поле TITLE. Критерии отбора не нужны. Все деньги в BYN"})

   response = client.chat.completions.create(
      model="deepseek-reasoner",
      messages=messages
   )

   from datetime import datetime
   total_deals = len(data)

   # Подсчет измененных сделок (где DATE_MODIFY != DATE_CREATE)
   modified_deals = 0

   for deal in data:
      create_date = datetime.strptime(deal["DATE_CREATE"], "%Y-%m-%dT%H:%M:%S+03:00")
      modify_date = datetime.strptime(deal["DATE_MODIFY"], "%Y-%m-%dT%H:%M:%S+03:00")
      
      if modify_date > create_date:
            modified_deals += 1

   # Расчет процента
   if total_deals == 0 or total_deals=='':
       total_deals=1

   percentage_modified = (modified_deals / total_deals) * 100
   requests.get('https://api.telegram.org/bot8136233806:AAGkSfMW81OkcKffxwcFuZVZul7-_n81My8/sendMessage?chat_id='+str(user)+'&text='
               +str(f"Процент измененных сделок: {percentage_modified:.2f}%\n")
               +str(f"Общее количество сделок: {total_deals}\n")
               +str(f"Измененных сделок: {modified_deals}\n\n\n")
               +str(response.choices[0].message.content)
               +'&parse_mode=html'
               )
   return 'f'