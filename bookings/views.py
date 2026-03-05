from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
from django.db.models import F, Sum

from .models import DarshanSlot, Booking

import qrcode
from io import BytesIO
from django.core.files import File


# ==============================
# BOOK DARSHAN (SAFE + REALTIME)
# ==============================
@login_required
def book_darshan(request, slot_id):
    # Get slot with temple
    slot = get_object_or_404(
        DarshanSlot.objects.select_related("temple"),
        id=slot_id
    )

    MAX_TICKETS_PER_USER = 5
    tickets_requested = 1  # currently 1 per booking (safe)

    # ✅ TOTAL tickets user already holds for this slot
    user_ticket_total = Booking.objects.filter(
        user=request.user,
        slot=slot,
        status='VALID'
    ).aggregate(total=Sum('ticket_count'))['total'] or 0

    # 🚫 enforce per-user limit
    if user_ticket_total >= MAX_TICKETS_PER_USER:
        messages.error(
            request,
            f"Maximum {MAX_TICKETS_PER_USER} tickets allowed for this slot."
        )
        return redirect('temple_detail', pk=slot.temple.id)

    if request.method == 'POST':
        with transaction.atomic():
            # 🔒 lock slot row
            slot = DarshanSlot.objects.select_for_update().get(id=slot_id)

            # 🚫 capacity check
            if slot.available_tickets < tickets_requested:
                messages.error(request, "This slot is fully booked.")
                return redirect('temple_detail', pk=slot.temple.id)

            # ✅ create booking
            booking = Booking.objects.create(
                user=request.user,
                slot=slot,
                ticket_count=tickets_requested
            )

            # ✅ update reserved safely
            slot.reserved_count = F('reserved_count') + tickets_requested
            slot.save()

        # =========================
        # QR GENERATION (unchanged)
        # =========================
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(str(booking.booking_id))
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')

        fname = f'qr-{booking.booking_id}.png'
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        booking.qr_code.save(fname, File(buffer), save=True)

        return redirect('booking_confirmation', booking_id=booking.booking_id)

    # GET request
    return render(request, 'bookings/book_confirm.html', {
        'slot': slot,
        'user_ticket_total': user_ticket_total,
        'max_allowed': MAX_TICKETS_PER_USER,
    })

# ==============================
# BOOKING CONFIRMATION
# ==============================
@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(
        Booking.objects.select_related("slot", "slot__temple", "user"),
        booking_id=booking_id,
        user=request.user
    )
    return render(request, 'bookings/booking_confirmation.html', {'booking': booking})


# ==============================
# MY BOOKINGS
# ==============================
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).select_related('slot', 'slot__temple').order_by('-slot__date')

    return render(request, 'bookings/history.html', {'bookings': bookings})


# ==============================
# CANCEL BOOKING (SAFE)
# ==============================
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        booking_id=booking_id,
        user=request.user
    )

    # 🚫 only future slots cancellable
    if booking.slot.date > timezone.localdate():
        with transaction.atomic():
            # lock slot
            slot = DarshanSlot.objects.select_for_update().get(id=booking.slot.id)

            booking.status = 'CANCELLED'
            booking.save()

            # safe decrement
            slot.reserved_count = F('reserved_count') - 1
            slot.save()

        messages.success(request, "Your Darshan booking has been successfully cancelled.")
    else:
        messages.error(request, "Cancellations are not allowed on or after the Darshan date.")

    return redirect('my_bookings')


# ==============================
# 🔴 REAL-TIME AVAILABILITY API
# (Temple-wise dynamic updates)
# ==============================
def slot_availability_api(request, slot_id):
    slot = get_object_or_404(DarshanSlot, id=slot_id)

    return JsonResponse({
        "available": slot.available_tickets,
        "reserved": slot.reserved_count,
        "capacity": slot.max_capacity,
        "temple": slot.temple.name,
        "date": slot.date,
        "slot_type": slot.slot_type,
    })