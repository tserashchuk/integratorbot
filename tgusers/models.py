from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    djuser = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField('Телефон', max_length=200, blank=True)
    tgid = models.CharField('айди телеги', max_length=200, blank=True)
    tgname = models.CharField('имя телеги', max_length=200, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.tgid
    
class ClientHook(models.Model):
    clientuser = models.ManyToManyField(Client)
    url = models.CharField('Телефон', max_length=200, blank=True)
    name = models.CharField('Имя', max_length=200, blank=True)

    def __str__(self):
        return self.name