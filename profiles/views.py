from django.shortcuts import render
from django.contrib import messages
from .models import Profile
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .utils import month_attendance_counter
from django.http import JsonResponse


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
