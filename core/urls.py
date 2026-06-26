from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookings.urls')), # This forwards empty routes to our app's urls.py
]