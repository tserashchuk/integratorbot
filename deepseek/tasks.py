from celery import shared_task
import requests
from datetime import date, datetime, timedelta
from tgusers.models import Client
from openai import OpenAI
from bitrix24 import *
from bs4 import BeautifulSoup
import re

@shared_task
def addf(user):
   myuser = Client.objects.get(tgid=user)
   myuser_hook = myuser.clientuser.all()
   # requests.get('https://api.telegram.org/bot8136233806:AAGkSfMW81OkcKffxwcFuZVZul7-_n81My8/sendMessage?chat_id=553875205&text='+str(myuser_hook[0].url))


   bx24 = Bitrix24(str(myuser_hook[0].url))
  
   data = bx24.callMethod('crm.deal.list',
                  filter={'CLOSED': 'N',
                           '>DATE_CREATE':'2025-03-31'},
                  select=['ID', 'TITLE', 'STAGE_ID','DATE_CREATE','DATE_MODIFY','CREATED_BY_ID','ASSIGNED_BY_ID','OPPORTUNITY','IS_RETURN_CUSTOMER','CONTACT_ID','CATEGORY_ID'])
   
   data = re.sub(r", ", ",", str(data))
   data = re.sub(r": ", ":", str(data))
   data = re.sub(r"'", "", str(data))
   
   client = OpenAI(api_key="sk-84f8be873ef144618d50838c7b548fcd", base_url="https://api.deepseek.com")
   messages=[
            {"role": "system", "content": 'представь что ты бизнес-аналитик. это данные из crm системы битрикс24, '+str(data)},
            {"role": "user", "content": 'систематизируй эти данные. для выделения курсива и жирного шрифта используй html теги без одинарных и двойных звездочек'}
      ]

   response = client.chat.completions.create(
      model="deepseek-chat",
      messages=messages
   )

   messages.append(response.choices[0].message)
   messages.append({"role": "user", "content": "выдели самые приоритетные сделки и напиши кому из лучше обработать. "
   "подготовь ответ на вопрос пользователя таким образом чтобы он был кратким - "
   "для выделения курсива и жирного шрифта используй html теги но не указывай их в сообщении, не используй одинарных и двоных звездочек. вообще не используй символ * "
   "Обрати внимание что название сделок хранится в поле TITLE. Критерии отбора и особенности ответа не нужны. Все деньги в BYN."
   "если направлений сделок несколько то выдели ТОП3 приоритетных для каждого направления сделок и сделай рекомендации для директора в кратком абзаце в конце"})


   response = client.chat.completions.create(
      model="deepseek-chat",
      messages=messages
   )


   requests.get('https://api.telegram.org/bot7216828718:AAFpVPusbLXoBYEWYpHg148EFBpPANGHdtk/sendMessage?chat_id='+str(user)+'&text='
               +str(response.choices[0].message.content)
               +'&parse_mode=html'
               )
   return 'f'


@shared_task
def reccomend(user,prompt):
   client = OpenAI(api_key="sk-84f8be873ef144618d50838c7b548fcd", base_url="https://api.deepseek.com")
   messages=[
            {"role": "system", "content": 'ты предприниматель с большим опытом работы и ты хочешь дать рекомендацию начинающему предпринимателю. сейчас ты работаешь на позиции CEO  McKinsey and Company '
            'для выделения жирным, курсивом и прочего оформления используй html теги вместо одинарных и двойных звездочек'},
            {"role": "user", "content": str(prompt)}
      ]
   response = client.chat.completions.create(
      model="deepseek-chat",
      messages=messages
   )
   requests.get('https://api.telegram.org/bot7216828718:AAFpVPusbLXoBYEWYpHg148EFBpPANGHdtk/sendMessage?chat_id='+str(user)+'&text='
               +str(response.choices[0].message.content)
               +'&parse_mode=html'
               )
   requests.get('https://api.telegram.org/bot7216828718:AAFpVPusbLXoBYEWYpHg148EFBpPANGHdtk/sendMessage?chat_id=553875205&text='
            +str(response.choices[0].message.content)
            +'&parse_mode=html'
            )
   return 'f'


@shared_task
def reccomend_event(user,prompt):

   client = OpenAI(api_key="sk-84f8be873ef144618d50838c7b548fcd", base_url="https://api.deepseek.com")
   messages=[
            {"role": "system", "content": 'ты предприниматель с большим опытом работы и ты хочешь дать рекомендацию начинающему предпринимателю. сейчас ты работаешь на позиции CEO  McKinsey and Company, '+str(data)},
            {"role": "user", "content": 'систематизируй эти данные. для выделения курсива и жирного шрифта используй html теги без одинарных и двойных звездочек'}
      ]

   response = client.chat.completions.create(
      model="deepseek-chat",
      messages=messages
   )

   messages.append(response.choices[0].message)
   messages.append({"role": "user", "content": str(prompt)})


   response = client.chat.completions.create(
      model="deepseek-chat",
      messages=messages
   )
   requests.get('https://api.telegram.org/bot7216828718:AAFpVPusbLXoBYEWYpHg148EFBpPANGHdtk/sendMessage?chat_id='+str(user)+'&text='
               +str(response.choices[0].message.content)
               +'&parse_mode=html'
               )
   requests.get('https://api.telegram.org/bot7216828718:AAFpVPusbLXoBYEWYpHg148EFBpPANGHdtk/sendMessage?chat_id=553875205&text='
            +str(response.choices[0].message.content)
            +'&parse_mode=html'
            )
   return 'f'