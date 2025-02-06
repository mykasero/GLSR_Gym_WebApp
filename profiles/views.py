from django.shortcuts import render
from django.contrib import messages
from .models import Profile, Payment
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .utils import month_attendance_counter, yearly_counter, this_month_activity, current_month_name, yearly_rank, monthly_rank, next_month, check_last_payment, reset_is_paid
from django.http import JsonResponse
from .forms import EmailForm, PfpForm, BlankForm, PaymentForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json
from datetime import datetime
from Schedule.views import staff_required
#profile page main view
@login_required(login_url="/login/")
def profile_home(request):
    if request.user.is_authenticated:
        # get profile id
        current_user = Profile.objects.get(user__id=request.user.id)
        # get all values by user id 
        user_info = Profile.objects.filter(user_id=request.user.id).values()
        # get the payment information for current user
        payment_info = Payment.objects.filter(user=request.user)
        
        context = {
            'user_info':user_info,
            'username': current_user, 
            'MEDIA_URL': settings.MEDIA_URL,
            'current_year' : datetime.now().year,
            'current_month' : current_month_name(datetime.now().month),
            'yearly_rank' : yearly_rank(current_user)[0],
            'yearly_rank_name' : yearly_rank(current_user)[1],
            'monthly_rank' : monthly_rank(current_user)[0],
            'monthly_rank_name' : monthly_rank(current_user)[1],
            'payment_info' : payment_info[0],
        }
        
        return render(request, "profiles/profile_home.html", {'context': context})
    else:
        # message - in order to access this view you need to be logged in
        messages.info(request, "Aby wejść w ten link musisz być zalogowany")
        return render(request, "Schedule/login.html")

# activity chart displayed on the profile page  
def profile_activity_chart(request):

    # get the profile id
    current_user = Profile.objects.get(user__id=request.user.id)

    # return a dict k:month, v:amount of bookings for the user
    booking_activity = month_attendance_counter(current_user) 
        
    # preparing variables for the chart
    labels = list(booking_activity.keys())
    data = list(booking_activity.values())
    
    return JsonResponse(data={
        'labels':labels,
        'data':data
    })

# view for modal to edit the users email information
@login_required(login_url="/login/")
def edit_email(request, pk):
    # get user based on the user id
    User_info = get_object_or_404(User, pk=pk)
    # get profile based on user id
    Profile_info = get_object_or_404(Profile, pk=pk)
    
    if request.method == "POST":
        form = EmailForm(request.POST, initial={
            'email' : User_info.email,
        })
        if form.is_valid():
            # change email in both user and profile model
            User_info.email = form.cleaned_data.get('email')
            Profile_info.email = form.cleaned_data.get('email')
            User_info.save()
            Profile_info.save()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "bookListChanged": None,
                        "showMessage": f"Zaktualizowano adres email."
                    })
                }
            )
        else:
            return render(request, 'profiles/email_form.html', {
                'form' : form,
                'email' : User_info.email,
            })
    else:
        form = EmailForm(initial={
            'email' : User_info.email,
        })
        return render(request, 'profiles/email_form.html', {
            'form' : form,
            'email' : User_info.email,
        })
    
# view for modal to edit the users profile picture
@login_required(login_url="/login/")
def edit_pfp(request, pk):
    # get profile by user id
    Profile_info = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        form = PfpForm(request.POST, request.FILES)
        
        if form.is_valid():
            Profile_info.profile_picture = form.cleaned_data.get('profile_picture')
            Profile_info.save()
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "bookListChanged": None,
                        "showMessage": f"Zaktualizowano zdjęcie profilowe."
                    })
                }
            )
        else:
            return render(request, 'profiles/pfp_form.html', {
                'form' : form,
                'profile_picture' : Profile_info.profile_picture,
            })
    else:
        form = PfpForm()
        return render(request, 'profiles/pfp_form.html', {
            'form' : form,
            'profile_picture' : Profile_info.profile_picture,
        })

# view for showing the information modal telling how the ranking system works
def rank_info(request):
    if request.method=="POST":
        form = BlankForm(request.POST)
        if form.is_valid():
            return render(request, 'profiles/profile_home.html')
        else:
            return render(request, 'profiles/rank_info.html', {'form' : form})
        
    else:
        form = BlankForm()    
        
    return render(request, 'profiles/rank_info.html', {'form':form})

# view for admin to manage the users subscriptions
@staff_required(login_url="/login/")
def payments(request):
    user_list_payments = Payment.objects.all()
    current_user = Profile.objects.get(user__id=request.user.id)
    user_list_info = check_last_payment(user_list_payments)
    
    
    # call a function that checks if users payment is expired and reset the is_paid attr
    reset_is_paid(user_list_info)
        
    
    context = {
        'current_user' : current_user,
        'user_list_payments' : user_list_info,
    }
    
    return render(request, 'profiles/payments.html', {'context':context})

# view for the modal to edit payments
@staff_required(login_url="/login/")
def edit_payments(request, pk):
    payment =  get_object_or_404(Payment, pk=pk)
    if request.method == "POST":
        form = PaymentForm(request.POST, initial={
            'is_paid' : payment.is_paid,
            'payment_date' : payment.payment_date,
        })
        if form.is_valid():
            payment.user = payment.user
            payment.is_paid = form.cleaned_data.get('is_paid')
            payment.payment_date = form.cleaned_data.get('payment_date')
            payment.expiry_date = next_month()
            payment.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger' : json.dumps({
                        "bookingListChanged" : None,
                        "showMessage" : f"Zaktualizowano status płatności"
                    })
                }
            )
        else:
            return render(request, 'profiles/payments_form.html', {
                'form' : form,
                'payment' : payment,
            })
        
        
    else:
        form = PaymentForm(request.POST, initial={
            'is_paid' : payment.is_paid,
            'payment_date' : payment.payment_date,
        })
    
        return render(request, 'profiles/payments_form.html', {
                'form' : form,
                'payment' : payment,
            })