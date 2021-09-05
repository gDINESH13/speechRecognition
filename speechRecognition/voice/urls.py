from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name="index"),  
    path('login',login_view,name="login"),
    path('register',register,name="register"),
     
    path('logout',logout_view,name="logout"),
    path('history',history,name="history"),
    path('textToSpeech',textToSpeech,name="textToSpeech"),
    path('getName',getName,name="getName"),
    path('renderNamePage',renderNamePage,name="renderNamePage"),
    path('getPreference/<str:name>',getPreference,name="getPreference")
]
