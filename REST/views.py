from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from Schedule.models import Booking, Archive
from REST.serializers import GroupSerializer, UserSerializer, BookingSerializer
from rest_framework.parsers import JSONParser
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
def Bookings_list(request):
    """
    List all bookings
    """
    
    if request.method == 'GET':
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings,many=True)
        return JsonResponse(serializer.data, safe = False)
    
    else:
        data = JSONParser().parse(request)
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors, status=400)
    
def Booking_detail(request, pk):
    """
    Retrieve, update or delete a booking
    """
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == "GET":
        serializer = BookingSerializer(booking)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookingSerializer(booking, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        booking.delete()
        return HttpResponse(status=204)
    
def Archives_list(request):
    """
    List all bookings
    """
    
    if request.method == 'GET':
        archives = Archive.objects.all()
        serializer = BookingSerializer(archives,many=True)
        return JsonResponse(serializer.data, safe = False)
    
    else:
        data = JSONParser().parse(request)
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors, status=400)
    
def Archive_detail(request, pk):
    """
    Retrieve, update or delete a booking
    """
    try:
        archive = Archive.objects.get(pk=pk)
    except Archive.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == "GET":
        serializer = BookingSerializer(archive)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = BookingSerializer(archive, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        archive.delete()
        return HttpResponse(status=204)