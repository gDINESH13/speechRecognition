from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name="index"),  
    path('login',login_view,name="login"),
    path('register',register,name="register"),
    path('speak',speak,name="speak"),  
    path('logout',logout_view,name="logout"),
    path('history',history,name="history"),
    path('textToSpeech',textToSpeech,name="textToSpeech")
]
