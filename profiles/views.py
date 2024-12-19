from django.shortcuts import render
from django.contrib import messages
from .models import Profile
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .utils import month_attendance_counter
from django.http import JsonResponse
from .forms import EmailForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json

@login_required(login_url="/login/")
def profile_home(request):
    if request.user.is_authenticated:
        # get profile id
        current_user = Profile.objects.get(user__id=request.user.id)
        # get all values by user id 
        user_info = Profile.objects.filter(user_id=request.user.id).values()
        # test_user_info = list(user_info)[0]
        context = {
            'user_info':user_info,
            'username': current_user, 
            'MEDIA_URL': settings.MEDIA_URL, 
        }

        # test what is inside of context
        # print(f"TEST request.user.id = {request.user.id} - - - {current_user} - - - {context}")
        
        # print(f"TEST function output - - - {month_attendance_counter(current_user)}")
        # booking_activity = month_attendance_counter(current_user) # returns a dict k:month, v:amount of bookings for the user
        
        return render(request, "profiles/profile_home.html", {'context': context})
    else:
        messages.info(request, "Aby wejść w ten link musisz być zalogowany")
        return render(request, "Schedule/login.html")
    
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

@login_required(login_url="/login/")
def edit_email(request, pk):
    User_info = get_object_or_404(User, pk=pk)
    Profile_info = get_object_or_404(Profile, pk=pk)
    if request.method == "POST":
        form = EmailForm(request.POST, initial={
            'email' : User_info.email,
        })
        if form.is_valid():
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
            return render(request, 'email_form.html', {
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