from django.urls import path
from . import views

urlpatterns = [
    path('book-slot/<int:slot_id>/', views.book_darshan, name='book_darshan'),
    path('confirmation/<uuid:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('my-history/', views.my_bookings, name='my_bookings'), # Added for D.7
    path('cancel/<uuid:booking_id>/', views.cancel_booking, name='cancel_booking'), # Added for D.8
    path(
    'slot-availability/<int:slot_id>/',
    views.slot_availability_api,
    name='slot_availability_api'
),
]