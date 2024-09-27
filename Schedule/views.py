import environ
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, BookingForm, BugReportForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import Group
from .models import Booking, Archive, Keycodes, BugReports
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test

#decorator for checking if logged user has staff permissions
def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url = login_url)

env = environ.Env()
environ.Env.read_env()

# Create your views here.

def home(request):
    #Homepage with 2 buttons, one for login page, one gallery
    
    return render(request, "Schedule/home.html")
    
def login(request, redirect_authenticated_user=True):
    #Login page
    if request.user.is_authenticated:
        return redirect('login_success/')
    else:
        
        if request.method == "POST":
            
            form = LoginForm()
            username = request.POST['login']
            password = request.POST['haslo']
            
            
            user = authenticate(request, username = username, password = password)
            if user is not None:
                auth_login(request,user)
                return redirect('login_success/')
            
            else:
                messages.error(request, "Podano niewłasciwe dane")
                return render(request,"Schedule/login.html", {'form' : form})
        else:
            if 'next' in request.GET:
                messages.warning(request, "Aby wyświetlić tą strone musisz być zalogowany")
            form = LoginForm()
            return render(request, "Schedule/login.html", {'form' : form})

@login_required(login_url="/login/")
def login_success(request):
    #View with current key stash code displaying upon login
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
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if request.POST['password1'] == "" or request.POST['password2'] == "" or \
            (request.POST['password1'] == "" and request.POST['password2'] == ""):
            
            if form.is_valid:
                messages.error(request, "Wypelnij pola od hasla")
                return render(request, "Schedule/register.html", {'form':form})

            else:
                form = RegisterForm()
                return render(request, "Schedule/register.html", {'form' : form})
            
        elif len(request.POST['password1']) < 8:
            messages.error(request, "Podane haslo jest za krotkie")
            return render(request, "Schedule/register.html", {'form':form})
        
        elif len(request.POST['username']) >= 50:
            messages.error(request, "Podano za długą nazwe użytkownika")
            return render(request, "Schedule/register.html", {'form' : form})
        
        
        elif request.POST['password1'] == request.POST['password2'] and request.POST['password1'] != "":  
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
            else:
                form = RegisterForm()
                return render(request, "Schedule/register.html", {'form' : form})
        
        else:
            messages.error(request, "Hasla nie sa identyczne")
            return render(request, "Schedule/register.html", {'form':form})
    
     
        return redirect("/")
    
    else:
        form = RegisterForm()
        return render(request, "Schedule/register.html", {'form':form})

@login_required(login_url="/login/")
def lobby(request):
    #Buttons move to schedule to book a hour or go to archive 
    return render(request, "Schedule/lobby.html")

@login_required(login_url="/login/")
def booking(request):
    #Creating a booking
    form = BookingForm() 
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
        
        form = BookingForm()     
        return render(request,'Schedule/booking.html', {'form':form})

@login_required(login_url="/login/")
def current_bookings(request):
    #Table with current bookings (today's date and up to 2 days after)
    
    context = Booking.objects.all().order_by('current_day')
    
    if context:
        return render(request, "Schedule/current_bookings.html", {'context' : context})
    else:
        return render(request, "Schedule/current_bookings.html")

@login_required(login_url="/login/")
def archive_booking(request):
    #Table with archived bookings, basic dataTables used for pagination and filtering
    context = Archive.objects.all().order_by('current_day')
    
    if context:
        return render(request, "Schedule/archive.html", {'context':context})
    else:
        messages.info(request, "No data available")
        return render(request, "Schedule/archive.html")

@login_required(login_url="/login/")
def bug_report(request):
    #View for making reports when a bug pops up
    form = BugReportForm()
    
    if request.method == "POST":
        form = BugReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Dziekujemy za złożenie zgłoszenia :)")
            return redirect('/')
    else:
        form = BugReportForm()
        return render(request, "Schedule/bug_report.html", {'form' : form})

@staff_required(login_url="/admin/")
def reports(request):
    #Datatables with user bug reports
    context = BugReports.objects.all().order_by('-report_date')
    
    if context:
        return render(request, "Schedule/reports.html", {'context' : context})
    else:
        messages.info(request, "Nie ma żadnych zgłoszeń :)")
        return render(request,"Schedule/reports.html")

def gallery(request):
    #View with a photo gallery of the gym
    return render(request, "Schedule/gallery.html")