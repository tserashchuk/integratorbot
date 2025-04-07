from django.db import models
from django.contrib.auth.models import User
from django_celery_beat.models import PeriodicTask

class ClientHook(models.Model):
    url = models.CharField('Вебхук', max_length=200, blank=True)
    name = models.CharField('Имя', max_length=200, blank=True)

    def __str__(self):
        return self.name
    
class Client(models.Model):
    djuser = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField('Телефон', max_length=200, blank=True)
    tgid = models.CharField('айди телеги', max_length=200, blank=True)
    tgname = models.CharField('имя телеги', max_length=200, blank=True)
    about = models.CharField('О компании', max_length=1000, blank=True)
    tasks = models.ManyToManyField(PeriodicTask)
    clientuser = models.ManyToManyField(ClientHook)

    def __str__(self):
        return self.tgid