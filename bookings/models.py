from django.db import models

class Inquiry(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    service_required = models.CharField(max_length=100)
    
    # New Field Added
    address = models.TextField(default="") 
    
    work_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.service_required}"