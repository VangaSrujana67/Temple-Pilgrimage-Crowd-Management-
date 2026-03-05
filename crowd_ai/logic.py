from .models import Festival, PublicHoliday, CrowdOverride
from bookings.models import DarshanSlot

def predict_crowd(temple, target_date):
    # 1. Check Admin Override (Requirement C.9)
    override = CrowdOverride.objects.filter(temple=temple, date=target_date).first()
    if override:
        return override.override_level, f"Manual Update: {override.reason}"

    # 2. Check Festival & Public Holidays (Requirement C.2)
    if Festival.objects.filter(date=target_date).exists():
        return "HIGH", "Festival Day - Traditional High Volume"
    
    if PublicHoliday.objects.filter(date=target_date).exists():
        return "HIGH", "Public Holiday - Expect Crowds"

    # 3. Check Weekend
    if target_date.weekday() >= 5:
        return "MEDIUM", "Weekend Flow"

    # 4. Check Historical/Current Booking Counts (Requirement C.2)
    slots = DarshanSlot.objects.filter(temple=temple, date=target_date)
    if slots.exists():
        total_capacity = sum(s.max_capacity for s in slots)
        total_reserved = sum(s.reserved_count for s in slots)
        utilization = (total_reserved / total_capacity) * 100 if total_capacity > 0 else 0
        
        if utilization > 80: return "HIGH", "Bookings nearly full"
        if utilization > 40: return "MEDIUM", "Steady booking rate"

    return "LOW", "Optimal time for Darshan"