from math import exp
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db import IntegrityError
import speech_recognition as sr
from django.contrib import messages
from .models import User,Chats
import pyttsx3
from django.contrib.auth.decorators import login_required



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



#list of all chats done 
@login_required
def history(request):
    chats=Chats.objects.filter(currentUser=request.user)
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

#records name of the person
@login_required
def getName(request):
    greetText='Hey there, Whats Your Name?'
    textToSpeech(greetText)
    audio=speechToText()

    try:
        
        #name of person
        name=r.recognize_google(audio)
    except:
        messages.error(request,'Failed to record voice Try again')
        #redirects to same page to record again
        return HttpResponseRedirect(reverse('renderNamePage'))
        
    # directs to getPreference page once name is recorded
    return render(request,'../templates/voice/getPreference.html',{'name':name})
    
#renders the page to record name
@login_required
def renderNamePage(request):
    return render(request,"../templates/voice/getName.html")

#records the preference of food by the user
@login_required
def getPreference(request,name):
    preference=f"Hey {name} What's your preference?"
    textToSpeech(preference)
    audio=speechToText()
    try:
        food=r.recognize_google(audio)   
    except:
        messages.error(request,"failed to record try again") 
        #renders back to main page to record name again
        return HttpResponseRedirect(reverse('renderNamePage'))

    #change text accoding to the preference of the user's
    if food.lower()=='nonveg' or food.lower()=='non veg':
        text=f"Hello {name} you prefered {food}, so I suggest You Chicken Burger."
    elif food.lower()=='veg' :
        text=f"Hello {name} you prefered {food}, so I suggest You Veg Burger."
    else:
        text=f"Hello {name} You prefered {food} But its not available."

    #final message if all reocdings are good.
    textToSpeech(text)
    #save text in database for managing history
    chat=Chats(text=text,spoke_by=name,currentUser=request.user)
    chat.save()
    #redirects to index page for next recoding
    return HttpResponseRedirect(reverse('index'))

    





    
        


    
    

 


