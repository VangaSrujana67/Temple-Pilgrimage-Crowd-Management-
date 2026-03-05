from django.shortcuts import redirect

def redirect_user_dashboard(user):
    return redirect('landing')
