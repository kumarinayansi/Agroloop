from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.landing_page, name='landing_page'),
    path('dashboard/', account_views.dashboard_view, name='dashboard'),
    path('auth/', include('django.contrib.auth.urls')), # Move auth to /auth/ to avoid conflict with /accounts/
    path('accounts/', include('accounts.urls')),
    path('tracking/', include('tracking.urls')),
    path('nutrition/', include('nutrition.urls')),
    path('redistribution/', include('redistribution.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
