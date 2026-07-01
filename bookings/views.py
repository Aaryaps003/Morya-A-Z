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
    # The exact unique URL generated on the client's phone
    ANDROID_GATEWAY_URL = "https://trigger.macrodroid.com/087923f4-3b14-474b-9290-ee5979e988de/morya-alert"
    
    try:
        # Professional WhatsApp Template with customer service sign-off
        professional_message = (
            f"🚨 *New Service Booking* 🚨\n\n"
            f"👤 *Customer:* {inquiry_data['full_name']}\n"
            f"📞 *Phone:* {inquiry_data['phone_number']}\n"
            f"🛠️ *Service:* {inquiry_data['service_required']}\n\n"
            f"📅 *Date:* {inquiry_data['preferred_date']}\n"
            f"🕒 *Slot:* {inquiry_data['preferred_slot']}\n\n"
            f"📍 *Address:*\n{inquiry_data['address']}\n\n"
            f"📝 *Details:*\n{inquiry_data['work_description']}\n\n"
            f"🙏 *Thank you for choosing Morya Housekeeping!*\n"
            f"👨‍💼 _Our representative will get in touch with you shortly._"
        )

        # Keys MUST match the Local Variables you created in the MacroDroid app
        payload = {
            "phone_number_var": inquiry_data['phone_number'],
            "message_content": professional_message
        }
        
        # 'params' automatically URL-encodes the emojis and line-breaks for MacroDroid!
        requests.get(ANDROID_GATEWAY_URL, params=payload, timeout=4)
        
    except Exception as e:
        print(f"Webhook delivery failed: {e}")

def homepage(request):
    return render(request, 'bookings/home.html')

def enquiry_page(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            # Save the inquiry to the Django database
            inquiry_instance = form.save()
            
            # --- PHONE NUMBER CLEANING ENGINE ---
            # 1. Remove any accidental spaces the user typed
            raw_phone = inquiry_instance.phone_number.strip().replace(" ", "")
            
            # 2. Smart check to append the Indian country code if missing
            if len(raw_phone) == 10 and raw_phone.isdigit():
                clean_phone = f"+91{raw_phone}"
            elif raw_phone.startswith("91") and len(raw_phone) == 12:
                clean_phone = f"+{raw_phone}"
            elif not raw_phone.startswith("+"):
                clean_phone = f"+91{raw_phone}"
            else:
                clean_phone = raw_phone
            # ------------------------------------
            
            # Package the data safely for the WhatsApp background task
            inquiry_data = {
                'full_name': inquiry_instance.full_name,
                'phone_number': clean_phone, # Sending the cleaned number!
                'service_required': inquiry_instance.service_required,
                'preferred_date': str(inquiry_instance.preferred_date),
                'preferred_slot': inquiry_instance.get_preferred_slot_display(),
                'address': inquiry_instance.address,
                'work_description': inquiry_instance.work_description
            }
            
            # Trigger the WhatsApp alert on a separate thread so the website doesn't freeze
            threading.Thread(target=_async_whatsapp_gateway_worker, args=(inquiry_data,), daemon=True).start()
            
            messages.success(request, "Thank you! Your booking enquiry has been recorded. Our team will contact you shortly.")
            return redirect('enquiry')
        else:
            print("❌ Validation Mismatch:", form.errors)
            messages.error(request, "Error processing submission parameters.")
    else:
        form = InquiryForm()
    
    context = get_shared_context()
    context['form'] = form
    return render(request, 'bookings/enquiry.html', context)