from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, logout_view, signup_view, verify_otp_view, user_dashboard, profile_settings

urlpatterns = [
    # Core Authentication
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),

    # Dashboards
    # path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/user/', user_dashboard, name='user_dashboard'),
    path('profile/', profile_settings, name='profile_settings'),

    # Standard Django Password Reset Flow (Aligned with SmartPilgrim templates)
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]