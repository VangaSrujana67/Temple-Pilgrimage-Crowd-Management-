import random
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum, Count

# Local App Imports
from .models import EmailOTP
from bookings.models import Booking
from contributions.models import Contribution
from safety.models import Notification, SOSAlert
from crowd_ai.logic import predict_crowd
from temples.models import Temple

User = get_user_model()

# --- AUTHENTICATION VIEWS ---

def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard' if request.user.role == 'admin' else 'user_dashboard')

    if request.method == 'POST':
        email = request.POST.get('username')  
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            if not user.is_active:
                messages.error(request, 'Verification required. Please verify your email.')
                request.session['verify_user'] = user.id
                return redirect('verify_otp')

            login(request, user)
            user.login_count += 1
            user.save(update_fields=['login_count'])
            return redirect('admin_dashboard' if user.role == 'admin' else 'user_dashboard')

        messages.error(request, 'Invalid divine credentials. Please try again.')
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'pilgrim')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'An account with this email already exists.')
            return redirect('login')

        user = User.objects.create_user(email=email, password=password, role=role, is_active=False)
        otp = str(random.randint(100000, 999999))
        EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp})

        try:
            send_mail(
                'Activate Your SmartPilgrim Account',
                f'Your secure OTP for SmartPilgrim is {otp}. Valid for 10 minutes.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            request.session['verify_user'] = user.id
            return redirect('verify_otp')
        except Exception:
            user.delete()
            messages.error(request, 'SMTP service failure. Account creation rolled back.')
            return redirect('signup')
    return render(request, 'accounts/signup.html')

def verify_otp_view(request):
    user_id = request.session.get('verify_user')
    if not user_id: return redirect('signup')
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(user=user).first()

        if otp_obj and not otp_obj.is_expired() and otp_obj.otp == entered_otp:
            user.is_active = True
            user.is_verified = True
            user.save()
            otp_obj.delete()
            del request.session['verify_user']
            return render(request, 'accounts/verify_success.html')
        
        messages.error(request, 'Invalid or expired token.')
        return render(request, 'accounts/verify_failed.html')
    return render(request, 'accounts/verify_otp.html')

# --- DASHBOARD VIEWS ---

@login_required
def user_dashboard(request):
    """Pilgrim Portal Logic (Requirement B)"""
    # Quick Actions & Summary (B.2, B.3)
    bookings = Booking.objects.filter(user=request.user, status='VALID').order_by('slot__date')
    total_dakshan = Contribution.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5]
    
    # AI Crowd Prediction for First Temple (Requirement B.4)
    t = Temple.objects.first()
    c_status, c_reason = predict_crowd(t, date.today()) if t else ("LOW", "Optimal for visit")

    return render(request, 'accounts/user_dashboard.html', {
        'bookings': bookings,
        'total_dakshan': total_dakshan,
        'notifications': notifications,
        'crowd_status': c_status,
        'crowd_reason': c_reason
    })


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Divine session ended securely.')
    return redirect('login')

@login_required
def profile_settings(request):
    if request.method == 'POST':
        user = request.user
        user.full_name = request.POST.get('full_name')
        user.phone_number = request.POST.get('phone_number')
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES.get('profile_picture')
        user.save()
        messages.success(request, "Your divine profile has been updated.")
        return redirect('profile_settings')
    
    return render(request, 'accounts/profile.html')