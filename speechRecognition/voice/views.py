from math import exp
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponse
import speech_recognition as sr
import pyaudio
from django.contrib import messages
from .models import User,Chats
import pyttsx3
import os

r=sr.Recognizer()

def index(request):
    if request.user.is_authenticated:
        return render(request,'../templates/voice/home.html')
    else:
        return HttpResponseRedirect(reverse('login'))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "../templates/voice/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "../templates/voice/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "../templates/voice/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "../templates/voice/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "../templates/voice/register.html")

# listens for user's name and preference and provides response
def speak(request):
    
    greetText='Hey there, Whats Your Name?'
    preference="What's your Preference?"
    textToSpeech(greetText)
    d={
        'name':'',
        'food':''
    }
    #listens for microphone noise
    audio=speechToText()

    try:
        #name of person
        name=r.recognize_google(audio)
        d['name']=name
        #ask for their preference
        textToSpeech(preference)
        audio=speechToText()
        #listen for their prefernce
        food=r.recognize_google(audio)
        d['food']=food
        # success if all went good
        messages.success(request,"Your voice is Recorded")
    except:
        #fails with error message 
        messages.error(request,'Failed to record voice')
        return  HttpResponseRedirect(reverse('index'))
    
    
    if d['name']!='' and d['food']!='':
        if d['food'].lower()=='nonveg' or d['food'].lower()=='non veg':
            text=f"Hello {d['name']} you prefered {d['food']}, so I suggest You Chicken Burger."
        elif d['food'].lower()=='veg' :
            text=f"Hello {d['name']} you prefered {d['food']}, so I suggest You Veg Burger."
        else:
            text=f"Hello {d['name']} You prefered {d['food']} But its not available."

        #storing in database for tracking past chats
        chat=Chats(text=text,spoke_by=request.user)
        chat.save()

        textToSpeech(text)
    return HttpResponseRedirect(reverse('index'))

#list of all chats done 
def history(request):
    chats=Chats.objects.filter(spoke_by=request.user)
    d={
        'chats':chats
    }

    return render(request,'../templates/voice/history.html',d)

#text to speech
def textToSpeech(text):
    engine=pyttsx3.init()
    engine.say(text)    
    engine.runAndWait()

# speech to text
def speechToText():
    
    with sr.Microphone() as source:
        audio=r.listen(source)
    return audio

    
    

 


