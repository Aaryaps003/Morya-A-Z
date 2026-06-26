from django.contrib import admin
from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    # This configures the columns displayed in the admin spreadsheet dashboard row
    list_display = ('full_name', 'phone_number', 'service_required', 'preferred_date', 'preferred_slot', 'created_at')
    
    # Adds a functional sidebar filter based on services and scheduled dates
    list_filter = ('service_required', 'preferred_date', 'preferred_slot')
    
    # Enables a rapid search bar for scanning names or numbers
    search_fields = ('full_name', 'phone_number', 'address')