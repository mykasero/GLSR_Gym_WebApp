from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

def home(request):
    #homepage with 2 buttons, one for login, one for guests moving to gallery (2nd TBD)
    
    
    return render(request, "Schedule/home.html")
    
def login(request):
    #login fields, login button, register hyperlink with text
    return HttpResponse("login")

def login_success(request):
    #different background, info that login is a success, buttons to booking/archive
    return HttpResponse("login_success")

def register(request):
    #register fields + access code known only to the group in order to eliminate not authorized people from 
    #making an account
    pass

def lobby(request):
    #TBD choice to move to schedule to book a hour
    pass

def booking(request):
    #booking, dropdown list of users(dynamic, when someone registers add user to this list),
    #text field for hours booked, add conversion from text to datetime so cleanup algorythm can
    #move the records into archive when the day passes 
    pass

def archive_booking(request):
    #maybe separate, idk TBD
    pass