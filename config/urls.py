from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
# A simple view for the landing page (Phase 1)
def landing_view(request):
    return render(request, 'landing.html')

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),
    
    # Public Pages
    path('', landing_view, name='landing'),
    
    # App-Specific Routes - UNCOMMENTED TO FIX REVERSE ERRORS
    path('accounts/', include('accounts.urls')),
    
    # # Placeholder for future apps
    path('temples/', include('temples.urls')),
    path('bookings/', include('bookings.urls')),
    # path('crowd-ai/', include('crowd_ai.urls')),
    path('contributions/', include('contributions.urls')),
    path('safety/', include('safety.urls')),
    path('management/', include('management.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)