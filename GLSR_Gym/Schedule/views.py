import environ
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Schedule.forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout

from .models import Booking

env = environ.Env()
environ.Env.read_env()

# Create your views here.

def home(request):
    #homepage with 2 buttons, one for login, one for guests moving to gallery
    
    return render(request, "Schedule/home.html")
    
def login(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST['login']
        password = request.POST['haslo']
        
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            auth_login(request,user)
            print("here")
            return redirect('login_success/')
        
        else:
            print("here2")
            return render(request,"Schedule/login.html", {'form' : form})
    
    return render(request, "Schedule/login.html", {'form' : form})

def login_success(request):
    #different background, info that login is a success, buttons to booking/archive
    
    return render(request,"Schedule/login_success.html")

def logout(request):
    auth_logout(request)
    messages.info(request, "Wylogowano pomyslnie")
    return redirect('/')

def register(request):
    #register fields + access code known only to the group in order to eliminate the possibility
    # of not authorized people from making an account
    
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:  
            form = RegisterForm(request.POST)
            print(request.POST)
            
            if form.is_valid:
                if request.POST['access_code'] == env("REGISTER_CODE"):
                    form.save()
                    
                # make another if for creating an admin account with a different register code
                
                elif request.POST['access_code'] != env("REGISTER_CODE"):
                    messages.error(request, "Podano zly kod dostepu.")
                    return render(request, "Schedule/register.html", {'form':form})
        
        else:
            return render(request, "Schedule/register.html", {'form':form})
        
        return redirect("/")
    else:
        form = RegisterForm()
        return render(request, "Schedule/register.html", {'form':form})

def lobby(request):
    #Buttons move to schedule to book a hour or go to archive
    
    return render(request, "Schedule/lobby.html")
def booking(request):
    
    
    return render(request,'Schedule/booking.html')

def current_bookings(request):
    #booking, dropdown list of users(dynamic, when someone registers add user to this list),
    #text field for hours booked, add conversion from text to datetime so cleanup algorythm can
    #move the records into archive when the day passes 
    
    context = Booking.objects.all()
    print("CONTEXT = \n",context)
    if context:
        print("context works")
        return render(request, "Schedule/current_bookings.html", {'context' : context})
    else:
        return render(request, "Schedule/current_bookings.html")

def archive_booking(request):
    #booking archive TBD - filtering specific periods maybe
    
    return render(request, "Schedule/archive.html")

def gallery(request):
    return render(request, "Schedule/gallery.html")