from django.shortcuts import render

def homepage(request):
    # Defining our core services dynamically in a list of dictionaries
    services = [
        {
            'title': 'Residential Cleaning',
            'description': 'Deep clean, routine maintenance, and move-in/move-out cleaning for your home.',
            'icon': '🏠'
        },
        {
            'title': 'Commercial & Office Cleaning',
            'description': 'Keep your workspace spotless, professional, and hygienic for your employees and clients.',
            'icon': '🏢'
        },
        {
            'title': 'Specialized Deep Cleaning',
            'description': 'Intense carpet washing, window treatment, and post-construction cleaning services.',
            'icon': '✨'
        }
    ]
    
    # Context data is passed as a dictionary to our HTML template
    context = {
        'firm_name': 'Morya A-Z Multi Services',
        'services': services
    }
    return render(request, 'bookings/home.html', context)