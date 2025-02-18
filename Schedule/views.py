import environ
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, BookingForm, BugReportForm, UserPasswordResetForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import Group
from .models import Booking, Archive, Keycodes, BugReports, CleaningSchedule, CleaningScheduleArchive
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
import json
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from profiles.models import Payment
from .decorators import user_is_active
# Dict with site names for dynamic message display
SITE_NAMES = {
    'booking' : 'rezerwacji',
    'current_bookings' : 'dzisiejszych rezerwacji',
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

#Homepage with 2 buttons, one for login page, one gallery
def home(request):
    return render(request, "Schedule/home.html")

# Login page view
def login(request):
    
    if request.user.is_authenticated:
        if 'next' in request.GET:
            if request.GET['next'][1:-1] == 'reports':
                if request.user.is_staff:
                    return render(request, 'Schedule/reports.html')
                else:
                    messages.warning(request, f"Aby wyświetlić strone {SITE_NAMES[request.GET['next'][1:-1]]} musisz być zalogowany jako administrator")
            else:
                return redirect('login_success/')
            
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
                    if dict(request.GET)['next'][0][1:-1] == 'reports' and not request.user.is_staff:
                        messages.warning(request, f"Aby wyświetlić strone {SITE_NAMES[dict(request.GET)['next'][0][1:-1]]} musisz być zalogowany jako administrator")
                    else:
                        messages.warning(request, f"Aby wyświetlić strone {SITE_NAMES[dict(request.GET)['next'][0][1:-1]]} musisz być zalogowany")
            
            form = LoginForm()
            return render(request, "Schedule/login.html", {'form' : form})

#View with current key stash code displaying upon login
@login_required(login_url="/login/")
def login_success(request):
    # Get the latest keycode
    keycode = list(Keycodes.objects.all().order_by('-id').values_list('code'))[0][0]
    
    user_payment_is_paid = Payment.objects.filter(user=request.user)[0].is_paid
    
    if user_payment_is_paid == True:
        # Display keycode upon successful login if user has paid
        messages.success(request, f"Kod do skrzynki z kluczem: {keycode}.") 
    else:
        messages.error(request, f"Aby uzyskać informację o kodzie do skrytki należy opłacić składke.")
    
    return render(request,"Schedule/login_success.html")


def logout(request):
    auth_logout(request)
    messages.info(request, "Wylogowano pomyslnie")
    return redirect('/')

#Registration page, access code known only to the group in order to eliminate the possibility
# of not authorized people from making an account
def register(request): 
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

# CBV for resetting forgotten password
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
    
# View with buttons that move to schedule to book a session, check current bookings or go to archive 
@login_required(login_url="/login/")
@user_is_active(redirect_url = "/login/")
def lobby(request):
    return render(request, "Schedule/lobby.html")

# View for booking reservations 
@login_required(login_url="/login/")
@user_is_active(redirect_url = "/login/")
def booking(request):
    form = BookingForm() 
    if request.method == "POST":
        form = BookingForm(request.POST)
        
        if form.is_valid():
            task_list = form.save(commit=False)
            # Fill the additional field with the booking users username
            task_list.created_by = request.user
            task_list.save()
            return redirect("/current_bookings")
        
        else:
            return render(request,'Schedule/booking.html', {'form':form})
    else:
        form = BookingForm()     
        return render(request,'Schedule/booking.html', {'form':form})
    

# View with a table with current bookings (booking gets moved to archive day after the specified date at ~1am)
@login_required(login_url="/login/")
@user_is_active(redirect_url = "/login/")
def current_bookings(request):
    context = Booking.objects.all().order_by('current_day')
    current_user = request.user.id
    
    if context:
        
        return render(request, "Schedule/current_bookings.html", {'context' : context, 'current_user' : current_user})
    
    return render(request, "Schedule/current_bookings.html", {'context':context})

# View for rendering the data in the table with current bookings
@login_required(login_url="/login/")
@user_is_active(redirect_url = "/login/")
def booking_list(request):
    context = Booking.objects.all()
    current_user = request.user.id
    return render(request,'Schedule/booking_list.html', {'context' : context, 'current_user' : current_user})

# View for the modal that renders a booking form which is used to edit the current booking
@login_required(login_url="/login/")
@user_is_active(redirect_url = "/login/")
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

# View for the modal that asks the user if he's sure that he wants to remove the booking
@login_required(login_url="/login/")
@user_is_active(redirect_url = "/login/")
def remove_booking_conf(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'Schedule/booking_delete_conf.html', {'booking' : booking})

# View for the modal that allows the user to remove his booking
@login_required(login_url="/login/")
@user_is_active(redirect_url = "/login/")
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

# View for a table with archived bookings, dataTables used for pagination and filtering 
# custom JS added to fix the default sort by date bug
@login_required(login_url="/login/")
@user_is_active(redirect_url = "/login/")
def archive_booking(request):
    context = Archive.objects.all()
    return render(request, "Schedule/archive.html", {'context':context})


#View with a form that allows users to report a bug
@login_required(login_url="/login/")
@user_is_active(redirect_url = "/login/")
def bug_report(request):
    
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

# View showing a datatable with user bug reports
@staff_required(login_url="/login/")
def reports(request):
    
    context = BugReports.objects.all().order_by('-report_date')
    
    return render(request, "Schedule/reports.html", {'context' : context})
 
#View with a photo gallery of the gym TBD(?)
def gallery(request):
    return render(request, "Schedule/gallery.html")

from Schedule.jobs import cleaning_user_roll
@login_required(login_url="/login/")
@user_is_active(redirect_url="/login/")
def cleaning_schedule(request):

    if CleaningSchedule.objects.all():
        currently_picked_user = list(CleaningSchedule.objects.all().order_by('-id').values_list('username'))[0][0]
    else:
        currently_picked_user = "---"
    
    cleaning_archive = CleaningScheduleArchive.objects.all().order_by('-id')
    
    if request.method == "POST":
        if 'roll_user' in request.POST:
            # test cleaning roll
            print("test start")
            print("przed losowaniem = ", CleaningSchedule.objects.all().values())
            print("archiwum przed = ", CleaningScheduleArchive.objects.all().values() )
            cleaning_user_roll()
            print("obecny user po losowaniu = ", CleaningSchedule.objects.all().values())
            print("archiwum po = ", CleaningScheduleArchive.objects.all().values())
            print("test end")
            
    
    context = {
        'currently_picked_user' : currently_picked_user,
        'cleaning_archive' : cleaning_archive,
    }
    
    return render(request,'Schedule/cleaning_schedule.html',{'context':context})