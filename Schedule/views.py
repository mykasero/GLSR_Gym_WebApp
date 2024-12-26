import environ
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, BookingForm, BugReportForm, UserPasswordResetForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import Group
from .models import Booking, Archive, Keycodes, BugReports
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
import json
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

SITE_NAMES = {
    'booking' : 'rezerwacji',
    'current_booking' : 'dzisiejszych rezerwacji',
    'archive' : 'archiwum',
    'reports' : 'zgłoszeń',
    'bug_report' : 'zgłoszenia problemu',
    'lobby' : 'poczekalni',
    'login/login_success' : 'ekranu powitalnego',
    
}

#decorator for checking if logged user has staff permissions
def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url = login_url)

env = environ.Env()
environ.Env.read_env()

def home(request):
    #Homepage with 2 buttons, one for login page, one gallery
    return render(request, "Schedule/home.html")
    
def login(request):
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
                if dict(request.GET)['next'][0][1:-1] in list(SITE_NAMES.keys()):  
                    messages.warning(request, f"Aby wyświetlić strone {SITE_NAMES[dict(request.GET)['next'][0][1:-1]]} musisz być zalogowany")
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

        if form.is_valid():
            if request.POST['access_code'] == env("REGISTER_CODE"):
                user = form.save()
                user.save()
                group = Group.objects.get(name='base_user')
                user.groups.add(group)
                messages.info(request, "Zarejestrowano pomyslnie")
                return redirect('/')
            
            elif request.POST['access_code'] == env("ADMIN_REGISTER_CODE"):
                user = form.save()
                user.is_staff = True
                user.save()
                group = Group.objects.get(name='admin_perm')
                user.groups.add(group)
                messages.info(request, "Zarejestrowano jako admin pomyslnie")
                return redirect('/')

        else:
            return render(request, "Schedule/register.html", {'form' : form})
    
    else:
        form = RegisterForm()
        return render(request, "Schedule/register.html", {'form':form})


from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "pass_reset/password_reset.html"
    email_template_name = "pass_reset/password_reset_email_body.html"
    subject_template_name = "pass_reset/password_reset_subject.txt"
    success_message = "Został wysłany na podany email link do resetowania hasła. " \
                        "Jeśli nie widzisz maila, sprawdź folder spam, w przypadku gdy tam " \
                        "również nie ma wiadomości - upewnij się czy podałeś poprawny adres email."
    form_class=UserPasswordResetForm
    success_url = reverse_lazy("home")

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        
        if user.is_authenticated and user.email and user.email != "twoj_email@gmail.com":
            initial['email'] = user.email
            initial['username'] = user.username
        elif user.is_authenticated:
            initial['username'] = user.username
            
        return initial

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            users = form.get_users(username)
            
            if users.exists():
                user = users.first()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                subject = f"Zmiana hasła dla {user} na stronie GLSR Gym"
                message = render_to_string(self.email_template_name,{
                    'email' : email,
                    'domain': request.get_host(),
                    'site_name': 'GLSR Gym',
                    'uid': uid,
                    'user': user,
                    'token': token,
                    'protocol': 'https' if request.is_secure() else 'http',
                })
                
                send_mail(subject, message,settings.DEFAULT_FROM_EMAIL, [email])
                
            
            return redirect(self.success_url)
        else:
            print("Form is invalid")
            return render(request, self.template_name, {'form':form})
    

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
            task_list = form.save(commit=False)
            task_list.created_by = request.user
            task_list.save()
            return redirect("/current_bookings")
        
        else:
            return render(request,'Schedule/booking.html', {'form':form})
    else:
        form = BookingForm()     
        return render(request,'Schedule/booking.html', {'form':form})
    


@login_required(login_url="/login/")
def current_bookings(request):
    #Table with current bookings (today's date and up to 2 days after)
    
    context = Booking.objects.all().order_by('current_day')
    current_user = request.user.id
    print(current_user)
    if context:
        return render(request, "Schedule/current_bookings.html", {'context' : context, 'current_user' : current_user})
    else:
        return render(request, "Schedule/current_bookings.html")

@login_required(login_url="/login/")
def booking_list(request):
    context = Booking.objects.all()
    current_user = request.user.id
    return render(request,'Schedule/booking_list.html', {'context' : context, 'current_user' : current_user})

@login_required(login_url="/login/")
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == "POST":
        form = BookingForm(request.POST, initial={
            'users' : booking.users,
            'users_amount' : booking.users_amount,
            'start_hour' : booking.start_hour,
            'end_hour' : booking.end_hour,
            'current_day' : booking.current_day,
        })
        if form.is_valid():
            booking.users = form.cleaned_data.get('users')
            booking.users_amount = form.cleaned_data.get('users_amount')
            booking.start_hour = form.cleaned_data.get('start_hour')
            booking.end_hour = form.cleaned_data.get('end_hour')
            booking.current_day = form.cleaned_data.get('current_day')
            booking.created_by = request.user
            booking.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger' : json.dumps({
                        "bookingListChanged" : None,
                        "showMessage" : f"Zaktualizowano rezerwacje"
                    })
                }
            )
        else:
            return render(request, 'Schedule/booking_form.html', {
                'form' : form,
                'booking' : booking,
            })
        
        
    else:
        form = BookingForm(initial={
            'users' : booking.users,
            'users_amount' : booking.users_amount,
            'start_hour' : booking.start_hour,
            'end_hour' : booking.end_hour,
            'current_day' : booking.current_day
        })
    
    return render(request, 'Schedule/booking_form.html', {
        'form' : form,
        'booking' : booking
        })

@login_required(login_url="/login/")
def remove_booking_conf(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'Schedule/booking_delete_conf.html', {'booking' : booking})

@login_required(login_url="/login/")
def remove_booking(request, pk):
    booking = get_object_or_404(Booking,pk=pk)
    booking.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger' : json.dumps({
                "bookingListChanged" : None,
                "showMessage" : f"Rezerwacja usunięta"
            })
        }
        )

@login_required(login_url="/login/")
def archive_booking(request):
    #Table with archived bookings, basic dataTables used for pagination and filtering
    context = Archive.objects.all()
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