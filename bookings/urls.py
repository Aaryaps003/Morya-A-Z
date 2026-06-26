from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('enquiry/', views.enquiry_page, name='enquiry'),
]