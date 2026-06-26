from django.shortcuts import render, redirect
from django.contrib import messages # Unit 3 Messages
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

def homepage(request):
    return render(request, 'bookings/home.html')

def enquiry_page(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your booking enquiry has been recorded. Our team will contact you shortly.")
            return redirect('enquiry')
    else:
        form = InquiryForm()
    
    context = get_shared_context()
    context['form'] = form
    return render(request, 'bookings/enquiry.html', context)