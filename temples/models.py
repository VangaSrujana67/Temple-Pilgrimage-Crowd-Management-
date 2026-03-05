from django.db import models

class Temple(models.Model):
    STATE_CHOICES = [
        ('AP', 'Andhra Pradesh'),
        ('TS', 'Telangana'),
        ('TN', 'Tamil Nadu'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        # Add more as needed
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deity = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    district = models.CharField(max_length=100)
    address = models.TextField()
    
    # Navigation/Map placeholders
    image = models.ImageField(upload_to='temple_images/')
    entry_gate_info = models.TextField(help_text="Instructions for Entry Gate")
    exit_gate_info = models.TextField(help_text="Instructions for Exit Gate")
    darshan_hall_info = models.TextField(help_text="Instructions for Darshan Hall")
    
    # Location for "Nearby" feature
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.district}"