from django import forms
from .models import Inquiry

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = [
            'full_name', 'phone_number', 'service_required', 
            'address', 'work_description', 'preferred_date', 'preferred_slot'
        ]