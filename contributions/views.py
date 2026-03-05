from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contribution
from temples.models import Temple
import uuid
from django.db.models import Sum  # Import this

@login_required
def donate_now(request):
    temples = Temple.objects.all()
    
    if request.method == 'POST':
        temple_id = request.POST.get('temple')
        amount = request.POST.get('amount')
        msg = request.POST.get('message')
        
        temple = Temple.objects.get(id=temple_id)
        
        # Create Mock Contribution (Requirement G.3)
        Contribution.objects.create(
            user=request.user,
            temple=temple,
            amount=amount,
            message=msg,
            transaction_id=f"TXN-{uuid.uuid4().hex[:10].upper()}"
        )
        
        messages.success(request, f"Your Dakshan for {temple.name} has been received. Thank you for your contribution!")
        return redirect('contribution_history')

    return render(request, 'contributions/donate.html', {'temples': temples})

@login_required
def contribution_history(request):
    # Fetch all donations for the current user
    donations = Contribution.objects.filter(user=request.user).order_by('-timestamp')
    
    # Calculate the lifetime total (Sum of the amount field)
    # aggregate returns a dictionary, e.g., {'amount__sum': 501}
    total_data = donations.aggregate(Sum('amount'))
    total_amount = total_data['amount__sum'] or 0.00
    
    context = {
        'donations': donations,
        'total_amount': total_amount,
    }
    
    return render(request, 'contributions/history.html', context)