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

# Create your views here.
def speak(request):
    r=sr.Recognizer()
    d={
        'output':''
    }
    
    with sr.Microphone() as source:
        audio=r.listen(source)

    try:
        output=r.recognize_google(audio)
        d['output']=output
        messages.success(request,"Your voice is Recorded")
    except:
        messages.error(request,'Failed to record voice')
    
    print(d['output'])
    if d['output']!='':
        chat=Chats(text=d['output'],spoke_by=request.user)
        chat.save()
    return HttpResponseRedirect(reverse('index'))

def history(request):
    chats=Chats.objects.filter(spoke_by=request.user)
    d={
        'chats':chats
    }

    return render(request,'../templates/voice/history.html',d)

 


