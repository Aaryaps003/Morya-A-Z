from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import threading

from .forms import InquiryForm

def get_shared_context():
    return {
        'categories': [
            {'name': 'Cleaning Solutions', 'icon': '✨', 'items': ['Full Home Deep Cleaning', 'Sofa & Carpet Shampooing', 'Water Tank Cleaning', 'Drainage & Leakage Solutions']},
            {'name': 'Technical & Repairs', 'icon': '⚡', 'items': ['All Electrical Works', 'All Plumbing Works', 'Home Appliances Repair', 'Water Motor & Borewell Installation']},
            {'name': 'Fabrication & Fitting', 'icon': '🔨', 'items': ['All Carpentry Work', 'Fitting Works (Glass, Tiles, Lights)', 'All Masonry Work', 'Gate Repair & Welding']},
            {'name': 'Outdoor & Garden', 'icon': '🏡', 'items': ['All Gardening Work', 'Lawn Maintenance & Landscaping']}
        ],
        'all_services': [
            'Residential Deep Cleaning', 'Commercial Cleaning', 'All Electrical Works', 
            'All Gardening Work', 'All Plumbing Works', 'Home Appliances Repair', 
            'Fitting Works (Glass, Tiles, Lights)', 'Water Motor & Borewell Services', 
            'Leakage Solutions', 'Gate Repair', 'All Carpentry Work', 'All Masonry Work'
        ]
    }

def _async_whatsapp_gateway_worker(inquiry_data):
    """Placeholder gateway thread worker until MacroDroid integration is configured"""
    ANDROID_GATEWAY_URL = "https://trigger.macrodroid.com/YOUR_UNIQUE_DEVICE_ID/morya-alert"
    try:
        # Structured payload distribution
        payload = {
            "customer_phone": inquiry_data['phone_number'],
            "message_content": f"🔔 New Inquiry: {inquiry_data['full_name']} wants {inquiry_data['service_required']}"
        }
        requests.post(ANDROID_GATEWAY_URL, json=payload, timeout=4)
    except Exception:
        pass # Silently proceed locally until device hooks are turned on

def homepage(request):
    return render(request, 'bookings/home.html')

def enquiry_page(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            # CRITICAL SAVE ROUTE: Commits entry row safely to SQLite
            inquiry_instance = form.save()
            
            # Map plain data vectors safely for the background worker thread payload
            inquiry_data = {
                'full_name': inquiry_instance.full_name,
                'phone_number': inquiry_instance.phone_number,
                'service_required': inquiry_instance.service_required,
                'preferred_date': str(inquiry_instance.preferred_date),
                'preferred_slot': inquiry_instance.get_preferred_slot_display(),
                'address': inquiry_instance.address,
                'work_description': inquiry_instance.work_description
            }
            
            threading.Thread(
                target=_async_whatsapp_gateway_worker, 
                args=(inquiry_data,), 
                daemon=True
            ).start()
            
            messages.success(request, "Thank you! Your booking enquiry has been recorded. Our team will contact you shortly.")
            return redirect('enquiry')
        else:
            # DIAGNOSTIC SAFETY: Outputs any mapping failures straight to your terminal window
            print("❌ FORM DATA VALIDATION FAILED! Errors encountered:", form.errors)
            messages.error(request, "There was an error processing your form data. Please check terminal outputs.")
    else:
        form = InquiryForm()
    
    context = get_shared_context()
    context['form'] = form
    return render(request, 'bookings/enquiry.html', context)