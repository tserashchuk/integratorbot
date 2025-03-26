"""
URL configuration for bitrixgpt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from tgusers import views as tview
from deepseek import views as dview

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', tview.Login.as_view(), name='login'),
    path('logout/', tview.Logout.as_view(), name='logout'),
    path('register/', tview.Register.as_view(), name='register'),
    path('cabinet/', tview.Cabinet.as_view(), name='cabinet'),
    path('addhook/', dview.AddHook.as_view(), name='addhook'),
]
