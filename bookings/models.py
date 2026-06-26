from django.db import models

class Inquiry(models.Model):
    # CharField translates to VARCHAR in database engines
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    service_required = models.CharField(max_length=100)
    
    # TextField handles large paragraphs of custom details
    work_description = models.TextField()
    
    # Auto-logs exactly when the customer hit the submit button
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.service_required}"