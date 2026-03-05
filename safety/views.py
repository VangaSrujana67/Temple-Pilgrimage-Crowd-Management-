from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SOSAlert, Notification

@login_required
def trigger_sos(request):
    if request.method == 'POST':
        issue = request.POST.get('issue_type')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        msg = request.POST.get('message', '')

        SOSAlert.objects.create(
            user=request.user,
            issue_type=issue,
            latitude=lat if lat else None,
            longitude=lng if lng else None,
            message=msg
        )
        
        # In a real scenario, this would trigger an SMS/Email to Admin
        messages.error(request, "EMERGENCY ALERT SENT! Please stay where you are, temple authorities have been notified.")
        return redirect('user_dashboard')

    return render(request, 'safety/sos_page.html')

@login_required
def notifications_list(request):
    # Requirement I.1/I.2: List format for alerts/reminders
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'safety/notifications.html', {'notifications': notes})

@login_required
def emergency_log(request):
    # Requirement H.5: Emergency request log for the user
    logs = SOSAlert.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'safety/sos_log.html', {'logs': logs})