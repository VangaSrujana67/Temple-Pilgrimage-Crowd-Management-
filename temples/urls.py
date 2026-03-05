from django.urls import path
from . import views

urlpatterns = [
    path('explore/', views.temple_list, name='temple_list'),
    path('explore/<int:pk>/', views.temple_detail, name='temple_detail'),
    path('nearby/', views.nearby_temples, name='nearby_temples'),
    path('live-detail/', views.live_temple_detail, name='live_temple_detail'),
]