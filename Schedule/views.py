import environ
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, BookingForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import Group
from .models import Booking, Archive, Keycodes
from django.contrib.auth import get_user_model




env = environ.Env()
environ.Env.read_env()

# Create your views here.

def home(request):
    #Homepage with 2 buttons, one for login page, one gallery
    
    return render(request, "Schedule/home.html")
    
def login(request):
    #Login page
    form = LoginForm()
    if request.method == "POST":
        username = request.POST['login']
        password = request.POST['haslo']
        
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            auth_login(request,user)
            return redirect('login_success/')
        
        else:
            messages.warning(request, "Podano niewłasciwe dane")#shows after succesful login, check it later
            return render(request,"Schedule/login.html", {'form' : form})
    
    return render(request, "Schedule/login.html", {'form' : form})

def login_success(request):
    keycode = list(Keycodes.objects.all().order_by('-id').values_list('code'))[0][0]
    messages.success(request, f"Kod do skrzynki z kluczem: {keycode}.") 
    return render(request,"Schedule/login_success.html")

def logout(request):
    auth_logout(request)
    messages.info(request, "Wylogowano pomyslnie")
    return redirect('/')

def register(request):
    #Registration page, access code known only to the group in order to eliminate the possibility
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
                
                elif request.POST['access_code'] == env("ADMIN_REGISTER_CODE"):
                    user = form.save()
                    user.is_staff = True
                    user.save()
                    group = Group.objects.get(name='admin_perm')
                    user.groups.add(group)
                    messages.info(request, "Zarejestrowano jako admin pomyslnie")
                
                elif request.POST['access_code'] not in  [env("REGISTER_CODE"),env("ADMIN_REGISTER_CODE")]:
                    messages.error(request, "Podano zly kod dostepu.")
                    return render(request, "Schedule/register.html", {'form':form})
        
        elif request.POST['password1'] == "" or request.POST['password2'] == "" or \
            (request.POST['password1'] == "" and request.POST['password2'] == ""):
            
            if form.is_valid:
                messages.error(request, "Wypelnij pola od hasla")
                return render(request, "Schedule/register.html", {'form':form})
        
        elif len(request.POST['password1']) < 8:
            messages.error(request, "Podane haslo jest za krotkie")
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
    #Page for creating a booking
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            users_list = User.objects.values('username')
            if form.cleaned_data['users'] in [value['username'] for value in list(users_list)]:
                form.save()
                return redirect("/current_bookings")
            else:
                messages.error(request, "Uzytkownik o takiej nazwie nie istnieje")
                return redirect('/booking')
    else:
        form = BookingForm(request.POST)     
        return render(request,'Schedule/booking.html', {'form':form})

def current_bookings(request):
    #Table with current bookings (today's date and up to 2 days after)
    
    context = Booking.objects.all().order_by('current_day')
    
    if context:
        return render(request, "Schedule/current_bookings.html", {'context' : context})
    else:
        return render(request, "Schedule/current_bookings.html")

def archive_booking(request):
    #Table with archived bookings, basic dataTables used for pagination and filtering
    context = Archive.objects.all().order_by('current_day')
    
    if context:
        return render(request, "Schedule/archive.html", {'context':context})
    else:
        messages.info(request, "No data available")
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