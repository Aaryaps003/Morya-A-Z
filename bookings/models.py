from django.db import models

class Inquiry(models.Model):
    TIME_SLOT_CHOICES = [
        ('morning', 'Morning (9:00 AM - 12:00 PM)'),
        ('afternoon', 'Afternoon (12:00 PM - 4:00 PM)'),
        ('evening', 'Evening (4:00 PM - 7:00 PM)'),
    ]

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    service_required = models.CharField(max_length=100)
    address = models.TextField(default="")
    work_description = models.TextField()
    preferred_date = models.DateField(null=True, blank=True)
    preferred_slot = models.CharField(max_length=20, choices=TIME_SLOT_CHOICES, default='morning')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.service_required}"