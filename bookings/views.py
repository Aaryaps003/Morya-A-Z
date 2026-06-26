from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import InquiryForm
from twilio.rest import Client  # Import the Twilio REST Client Engine
import os

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

def send_whatsapp_alert(inquiry_instance):
    """
    Helper function to execute event-driven communication out of Django
    """
    # Grab free credentials from your Twilio Console Dashboard
    # In production, store these safely in a .env file (Unit 5 best practices)
    account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    
    try:
        client = Client(account_sid, auth_token)
        
        # Format the notification string beautifully for the business owner
        alert_message = (
            f"🔔 *New Inquiry on Morya A-Z!* \n\n"
            f"👤 *Client:* {inquiry_instance.full_name}\n"
            f"📞 *Phone:* {inquiry_instance.phone_number}\n"
            f"🛠️ *Service:* {inquiry_instance.service_required}\n"
            f"📅 *Schedule:* {inquiry_instance.preferred_date} ({inquiry_instance.preferred_slot})\n"
            f"📍 *Address:* {inquiry_instance.address}\n"
            f"📝 *Details:* {inquiry_instance.work_description}"
        )
        
        # Fire message using Twilio's Sandbox system channel
        message = client.messages.create(
            from_='whatsapp:+14155238886',  # Standard Twilio Sandbox sandbox number
            body=alert_message,
            to=f'whatsapp:+919021220673'    # Your registered personal WhatsApp number
        )
        print(f"WhatsApp notification triggered successfully: {message.sid}")
    except Exception as e:
        print(f"Automation transmission skipped or failed: {e}")

def homepage(request):
    return render(request, 'bookings/home.html')

def enquiry_page(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            # Save row data to SQLite database
            inquiry_instance = form.save()
            
            # Fire the instant background automated message alert!
            send_whatsapp_alert(inquiry_instance)
            
            messages.success(request, "Thank you! Your booking enquiry has been recorded. An admin will contact you shortly.")
            return redirect('enquiry')
    else:
        form = InquiryForm()
    
    context = get_shared_context()
    context['form'] = form
    return render(request, 'bookings/enquiry.html', context)