from django.shortcuts import render, redirect
from django.http import HttpResponse
from Schedule.forms import LoginForm, RegisterForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def home(request):
    #homepage with 2 buttons, one for login, one for guests moving to gallery (2nd TBD)
    # context = {}
    # form = BookingForm
    # booking = Booking.objects.all()
    # context['users'] = booking
    # context['title'] = 'test1'
    # context['form'] = form
    
    return render(request, "Schedule/home.html")
    
# def login(request):
#     #login fields, login button, register hyperlink with text
#     form = LoginForm()

#     return render(request, "Schedule/login.html", {'form' : form})

def login(request):
    form = LoginForm()
    if request.method == "POST":
        
        print("LOGIN TEST ---- ",request.POST['login'], request.POST['haslo'])
        username = request.POST['login']
        password = request.POST['haslo']
        user = authenticate(request, username = username, password = password)
        print("user - ", user)
        if user is not None:
            auth_login(request,user)
            print("here")
            return redirect('login_success.html')
        else:
            print("here2")
            return render(request,"Schedule/login.html", {'form' : form})
    return render(request, "Schedule/login.html", {'form' : form})

def login_success(request):
    #different background, info that login is a success, buttons to booking/archive
    return render(request,"Schedule/login_success.html")

# add logout as well

def register(request):
    #register fields + access code known only to the group in order to eliminate the possibility
    # of not authorized people from making an account
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:  
            form = RegisterForm(request.POST)
            print(request.POST)
            
            if form.is_valid:
                if request.POST['access_code'] == "123":
                    form.save()
                
                elif request.POST['access_code'] != "123":
                    print("WRONG ACCESS CODE")
                    return render(request, "Schedule/register.html", {'form':form})
        
        else:
            print("PASSWORDS NOT THE SAME")
            return render(request, "Schedule/register.html", {'form':form})
        
        return redirect("/")
    else:
        form = RegisterForm()
        return render(request, "Schedule/register.html", {'form':form})

def lobby(request):
    #TBD choice to move to schedule to book a hour or go to archive
    pass

def booking(request):
    #booking, dropdown list of users(dynamic, when someone registers add user to this list),
    #text field for hours booked, add conversion from text to datetime so cleanup algorythm can
    #move the records into archive when the day passes 
    pass

def archive_booking(request):
    #maybe separate, idk TBD
    pass