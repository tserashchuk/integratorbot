from celery import shared_task
import requests
from datetime import date, datetime, timedelta

@shared_task
def add():
   return 'f'