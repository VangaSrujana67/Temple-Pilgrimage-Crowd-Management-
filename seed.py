import os
import django
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from temples.models import Temple
from bookings.models import DarshanSlot, Booking
from contributions.models import Contribution
from safety.models import Notification, SOSAlert
from crowd_ai.models import Festival

User = get_user_model()

print("\n========= SMART PILGRIM DATA SEED START =========\n")

# =====================================================
# 1. USERS
# =====================================================

admin, created = User.objects.get_or_create(
    email="admin@smartpilgrim.com",
    defaults={
        "full_name": "Chief Administrator",
        "role": "admin",
        "is_staff": True,
        "is_superuser": True,
        "is_active": True,
    },
)

if created:
    admin.set_password("admin123")
    admin.save()

pilgrim, created = User.objects.get_or_create(
    email="devotee@smartpilgrim.com",
    defaults={
        "full_name": "P. Hari Sai",
        "role": "pilgrim",
        "is_active": True,
    },
)

if created:
    pilgrim.set_password("user123")
    pilgrim.save()

print("Users ready.")

# =====================================================
# 2. TEMPLES
# =====================================================

temple_data = [
    {
        "name": "Sri Venkateswara Swamy Temple",
        "district": "Tirupati",
        "state": "AP",
        "deity": "Lord Venkateswara",
        "latitude": 13.6833,
        "longitude": 79.3500,
        "description": "Ancient hill temple."
    },
    {
        "name": "Yadadri Lakshmi Narasimha Temple",
        "district": "Yadadri Bhuvanagiri",
        "state": "TS",
        "deity": "Lord Narasimha",
        "latitude": 17.5875,
        "longitude": 78.9397,
        "description": "Magnificent cave temple."
    },
]

for t in temple_data:
    Temple.objects.get_or_create(
        name=t["name"],
        defaults={
            "district": t["district"],
            "state": t["state"],
            "deity": t["deity"],
            "latitude": t["latitude"],
            "longitude": t["longitude"],
            "description": t["description"],
            "entry_gate_info": "Main Entrance",
            "darshan_hall_info": "Central Hall",
            "exit_gate_info": "North Exit",
        },
    )

print("Temples ready.")

# =====================================================
# 3. FESTIVALS
# =====================================================

Festival.objects.get_or_create(
    name="Maha Shivaratri",
    date=date.today() + timedelta(days=7),
)

Festival.objects.get_or_create(
    name="Vaikunta Ekadasi",
    date=date.today() + timedelta(days=15),
)

print("Festivals ready.")

# =====================================================
# 4. DARSHAN SLOTS
# =====================================================

slot_types = ["MORNING", "AFTERNOON", "NIGHT"]

for temple in Temple.objects.all():
    for day in [date.today(), date.today() + timedelta(days=1)]:
        for slot_type in slot_types:
            DarshanSlot.objects.get_or_create(
                temple=temple,
                date=day,
                slot_type=slot_type,
                defaults={
                    "max_capacity": 100,
                    "reserved_count": 0,
                },
            )

print("Slots ready.")

# =====================================================
# 5. SAMPLE BOOKING
# =====================================================

slot = DarshanSlot.objects.first()

if slot:
    booking, created = Booking.objects.get_or_create(
        user=pilgrim,
        slot=slot,
        defaults={
            "ticket_count": 2,
            "status": "VALID",
        },
    )

    if created:
        slot.reserved_count += 2
        slot.save()

print("Sample booking ready.")

# =====================================================
# 6. CONTRIBUTIONS
# =====================================================

temple = Temple.objects.first()

if temple:
    Contribution.objects.get_or_create(
        user=pilgrim,
        temple=temple,
        amount=501,
        message="Om Namo Venkatesaya",
    )

print("Contributions ready.")

# =====================================================
# 7. NOTIFICATIONS
# =====================================================

Notification.objects.get_or_create(
    user=pilgrim,
    title="Booking Confirmed",
    message="Your darshan booking is valid.",
)

Notification.objects.get_or_create(
    user=pilgrim,
    title="Crowd Alert",
    message="High crowd expected due to festival.",
)

print("Notifications ready.")

# =====================================================
# 8. SOS
# =====================================================

SOSAlert.objects.get_or_create(
    user=pilgrim,
    issue_type="MEDICAL",
    message="Feeling unwell near main hall.",
    status="PENDING",
    latitude=13.6833,
    longitude=79.3500,
)

print("SOS ready.")

print("\n========= SMART PILGRIM DATA SEED COMPLETE =========\n")
