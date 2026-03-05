from django.urls import path
from . import views

urlpatterns = [
    path('sos/', views.trigger_sos, name='trigger_sos'),
    path('sos/log/', views.emergency_log, name='emergency_log'),
    path('notifications/', views.notifications_list, name='notifications'),
]