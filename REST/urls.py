from django.urls import path
from REST import views

urlpatterns = [
    path('current_bookings/list/', views.Bookings_list),
    path('current_bookings/list/<int:pk>/', views.Booking_detail),
    path('archive/list/', views.Archives_list),
    path('archive/list/<int:pk>/', views.Archive_detail),
]
