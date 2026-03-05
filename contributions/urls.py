from django.urls import path
from . import views

urlpatterns = [
    path('donate/', views.donate_now, name='donate_now'),
    path('history/', views.contribution_history, name='contribution_history'),
]