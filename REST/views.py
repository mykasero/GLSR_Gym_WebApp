from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from Schedule.models import Booking, Archive
from REST.serializers import GroupSerializer, UserSerializer, BookingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
    
@api_view(['GET','POST'])
def Bookings_list(request, format= None):
    """
    List all bookings
    """
    
    if request.method == 'GET':
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings,many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])    
def Booking_detail(request, pk, format= None):
    """
    Retrieve, update or delete a booking
    """
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])    
def Archives_list(request, format= None):
    """
    List all bookings
    """
    
    if request.method == 'GET':
        archives = Archive.objects.all()
        serializer = BookingSerializer(archives,many=True)
        return Response(serializer.data)
    
    else:
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])      
def Archive_detail(request, pk, format= None):
    """
    Retrieve, update or delete a booking
    """
    try:
        archive = Archive.objects.get(pk=pk)
    except Archive.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = BookingSerializer(archive)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = BookingSerializer(archive, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        archive.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)