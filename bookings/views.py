import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import InquiryForm
import threading

# ... keep your get_shared_context and homepage views exactly the same ...

def _async_whatsapp_gateway_worker(inquiry_data):
    """
    Production-Grade Local Gateway Client.
    Dispatches form data directly to your local Android automator webhook.
    """
    # Replace this with the unique Webhook URL given to you by MacroDroid / Tasker
    ANDROID_GATEWAY_URL = "https://trigger.macrodroid.com/YOUR_UNIQUE_DEVICE_ID/morya-alert"
    
    # Structure a clean, clean text payload matching your branding
    alert_body = (
        f"🔔 *New Inquiry Received!* \n\n"
        f"👤 *Client:* {inquiry_data['full_name']}\n"
        f"📞 *Phone:* {inquiry_data['phone_number']}\n"
        f"🛠️ *Service:* {inquiry_data['service_required']}\n"
        f"📅 *Schedule:* {inquiry_data['preferred_date']} ({inquiry_data['preferred_slot']})\n"
        f"📍 *Address:* {inquiry_data['address']}\n"
        f"📝 *Details:* {inquiry_data['work_description']}"
    )
    
    payload = {
        "customer_phone": inquiry_data['phone_number'],
        "message_content": alert_body
    }
    
    try:
        # Fire the network request to your Android device with a crisp 5-second timeout
        response = requests.post(ANDROID_GATEWAY_URL, json=payload, timeout=5)
        print(f"[GATEWAY LOG] Data successfully dispatched to Android device: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[GATEWAY ERROR] Could not connect to Android device pipeline: {e}")

def enquiry_page(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry_instance = form.save()
            
            inquiry_data = {
                'full_name': inquiry_instance.full_name,
                'phone_number': inquiry_instance.phone_number,
                'service_required': inquiry_instance.service_required,
                'preferred_date': str(inquiry_instance.preferred_date),
                'preferred_slot': inquiry_instance.get_preferred_slot_display(),
                'address': inquiry_instance.address,
                'work_description': inquiry_instance.work_description
            }
            
            # Spin off the network webhook call to a background thread
            threading.Thread(
                target=_async_whatsapp_gateway_worker, 
                args=(inquiry_data,), 
                daemon=True
            ).start()
            
            messages.success(request, "Thank you! Your booking enquiry has been recorded. Our team will contact you shortly.")
            return redirect('enquiry')
    else:
        form = InquiryForm()
    
    context = get_shared_context()
    context['form'] = form
    return render(request, 'bookings/enquiry.html', context)