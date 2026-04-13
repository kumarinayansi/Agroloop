from django.urls import path
from . import views

urlpatterns = [
    path('', views.batch_list, name='batch_list'),
    path('batch/<uuid:batch_id>/', views.batch_detail, name='batch_detail'),
    path('batch/create/', views.batch_create, name='batch_create'),
    path('batch/<uuid:batch_id>/qr/', views.generate_qr_view, name='generate_qr'),
    path('batch/<uuid:batch_id>/log/', views.add_journey_log, name='add_journey_log'),
]
