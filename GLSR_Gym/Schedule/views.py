from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    #homepage with 2 buttons, one for login, one for guests moving to gallery (2nd TBD)
    
    pass
    #return HttpResponse("First test")
    
def login(request):
    #login fields, login button, register hyperlink with text
    pass

def register(request):
    #register fields + access code known only to the group in order to eliminate not authorized people from 
    #making an account
    pass

def lobby(request):
    #TBD choice to move to schedule to book a hour
    pass

def booking(request):
    #booking, dropdown list of users(dynamic, when someone registers add user to this list),
    #text field for hours booked
    pass