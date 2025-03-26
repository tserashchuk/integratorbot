from django.contrib import admin
from tgusers.models import *


admin.site.register(Client, admin.ModelAdmin)
admin.site.register(ClientHook, admin.ModelAdmin)