from django.db import models
from django.conf import settings
from temples.models import Temple
import uuid

class DarshanSlot(models.Model):
    SLOT_CHOICES = [
        ('MORNING', 'Morning (6 AM - 11 AM)'),
        ('AFTERNOON', 'Afternoon (12 PM - 4 PM)'),
        ('NIGHT', 'Night (5 PM - 9 PM)'),
    ]
    
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE)
    date = models.DateField()
    slot_type = models.CharField(max_length=10, choices=SLOT_CHOICES)
    max_capacity = models.PositiveIntegerField(default=100)
    reserved_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('temple', 'date', 'slot_type')

    @property
    def available_tickets(self):
        return self.max_capacity - self.reserved_count

    def __str__(self):
        return f"{self.temple.name} - {self.date} ({self.slot_type})"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('VALID', 'Valid'),
        ('USED', 'Used/Scanned'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slot = models.ForeignKey(DarshanSlot, on_delete=models.CASCADE)
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    ticket_count = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='VALID')
    booked_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True)

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.email}"