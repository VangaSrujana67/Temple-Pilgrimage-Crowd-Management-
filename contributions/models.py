from django.db import models
from django.conf import settings
from temples.models import Temple

class Contribution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    temple = models.ForeignKey(Temple, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    message = models.TextField(blank=True, help_text="Optional prayer or message")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dakshan of ₹{self.amount} for {self.temple.name}"