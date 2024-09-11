import environ
from django.shortcuts import render, redirect
from django.http import HttpResponse
from Schedule.forms import LoginForm, RegisterForm, BookingForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import Group
from .models import Booking, Archive
import datetime


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
            return redirect('login_success/')
        
        else:
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
        form = RegisterForm(request.POST)
    
        if request.POST['password1'] == request.POST['password2'] and request.POST['password1'] != "":  
            if form.is_valid:
                if request.POST['access_code'] == env("REGISTER_CODE"):
                    user = form.save()
                    user.save()
                    group = Group.objects.get(name='base_user')
                    user.groups.add(group)
                    messages.info(request, "Zarejestrowano pomyslnie")
                
                elif request.POST['access_code'] == "54321":
                    user = form.save()
                    user.is_staff = True
                    user.save()
                    group = Group.objects.get(name='admin_perm')
                    user.groups.add(group)
                    messages.info(request, "Zarejestrowano jako admin pomyslnie")
                        
                # make another if for creating an admin account with a different register code
                
                elif request.POST['access_code'] != env("REGISTER_CODE"):
                    messages.error(request, "Podano zly kod dostepu.")
                    return render(request, "Schedule/register.html", {'form':form})
        
        elif request.POST['password1'] == "" or request.POST['password2'] == "" or \
            (request.POST['password1'] == "" and request.POST['password2'] == ""):
            
            if form.is_valid:
                messages.error(request, "Wypelnij pola od hasla")
                return render(request, "Schedule/register.html", {'form':form})
        else:
            messages.error(request, "Hasla nie sa identyczne")
            return render(request, "Schedule/register.html", {'form':form})
        
        return redirect("/")
    
    else:
        form = RegisterForm()
        return render(request, "Schedule/register.html", {'form':form})

def lobby(request):
    #Buttons move to schedule to book a hour or go to archive
    
    return render(request, "Schedule/lobby.html")

def booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        print("tu1")
        if form.is_valid():
            print("tu3")
            form.save()    
            return redirect("/current_bookings")
    else:
        form = BookingForm(request.POST)     
        print("tu2")   
        return render(request,'Schedule/booking.html', {'form':form})

def current_bookings(request):
    #booking, dropdown list of users(dynamic, when someone registers add user to this list),
    #text field for hours booked, add conversion from text to datetime so cleanup algorythm can
    #move the records into archive when the day passes 
    
    context = Booking.objects.all().order_by('current_day')
    
    if context:
        return render(request, "Schedule/current_bookings.html", {'context' : context})
    else:
        return render(request, "Schedule/current_bookings.html")

def archive_booking(request):
    #booking archive TBD - filtering specific periods maybe
    context = Archive.objects.all().order_by('current_day')
    
    if context:
        return render(request, "Schedule/archive.html", {'context':context})
    else:
        messages.info("No data available")
        return render(request, "Schedule/archive.html")
def test_dtables(request):
    context = Archive.objects.all().order_by('current_day')
    
    if context:
        return render(request, "Schedule/test_dtables.html", {'context':context})
    else:
        messages.info("No data available")
        return render(request, "Schedule/test_dtables.html")

def gallery(request):
    return render(request, "Schedule/gallery.html")