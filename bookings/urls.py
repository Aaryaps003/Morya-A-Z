from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'), # Maps the root domain to our homepage view
]