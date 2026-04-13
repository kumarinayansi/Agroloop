from django.urls import path
from . import views

urlpatterns = [
    path('', views.scanner_home, name='scanner_home'),
    path('scan/', views.scan_product, name='scan_product'),
]
