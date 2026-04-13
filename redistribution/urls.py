from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('<int:pk>/', views.listing_detail, name='listing_detail'),
    path('create/', views.listing_create, name='listing_create'),
    path('<int:listing_id>/claim/', views.claim_listing, name='claim_listing'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('listing/<int:listing_id>/claim/quick/', views.quick_claim, name='quick_claim'),
]
