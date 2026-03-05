from django.db import models
from django.conf import settings

class SOSAlert(models.Model):
    ISSUE_CHOICES = [
        ('MEDICAL', 'Medical Emergency'),
        ('CROWD', 'Crowd Suffocation/Crush'),
        ('SAFETY', 'Harassment/Safety Threat'),
        ('LOST', 'Missing Person/Child'),
        ('OTHER', 'Other Urgent Issue'),
    ]
    STATUS_CHOICES = [('PENDING', 'Pending'), ('RESOLVED', 'Resolved')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=20, choices=ISSUE_CHOICES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SOS: {self.issue_type} by {self.user.email}"

class Notification(models.Model):
    CAT_CHOICES = [('REMINDER', 'Darshan Reminder'), ('CROWD', 'Crowd Alert'), ('INFO', 'System Update')]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CAT_CHOICES, default='INFO')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category}: {self.title}"