from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tracking.models import Batch
from redistribution.models import FoodListing, Claim
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account is ready.")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def landing_page(request):
    return render(request, 'landing.html')


from nutrition.models import ScanHistory

from django.db.models import Sum

@login_required
def dashboard_view(request):
    role = request.user.role
    context = {'role': role}
    
    # ── SHARED DATA ────────────────────────────────────────────────────────
    now = timezone.now()
    urgency_threshold = now + timedelta(hours=2)
    listings_available = FoodListing.objects.filter(status='AVAILABLE', expiry_window__gt=now).select_related('listed_by')

    # ── ROLE-SPECIFIC LOGIC ──────────────────────────────────────────────────
    
    if role == 'FARMER':
        user_batches = Batch.objects.filter(farmer=request.user)
        context.update({
            'total_batches': user_batches.count(),
            'active_batches': user_batches.exclude(current_status='SOLD').count(),
            'yield_total': user_batches.aggregate(Sum('quantity_kg'))['quantity_kg__sum'] or 0,
            'recent_batches': user_batches.order_by('-created_at')[:5],
        })

    elif role == 'NGO':
        user_claims = Claim.objects.filter(claimant=request.user)
        context.update({
            'available_donations': listings_available.count(),
            'claimed_meals': user_claims.count(),
            'total_claims_pending': user_claims.filter(status='PENDING').count(),
            'recent_claims': user_claims.select_related('listing').order_by('-claimed_at')[:5],
            'recent_listings': listings_available.order_by('expiry_window')[:5],
        })

    elif role == 'CONSUMER':
        scans = ScanHistory.objects.filter(user=request.user)
        total_scans = scans.count()
        stats = {'healthy': 0, 'sugar': 0, 'alerts': 0}
        if total_scans > 0:
            stats['healthy'] = scans.filter(nutriscore_grade__in=['A', 'B'], health_alerts_count=0).count()
            stats['sugar'] = scans.filter(has_high_sugar=True).count()
            stats['alerts'] = scans.filter(health_alerts_count__gt=0).exclude(has_high_sugar=True).count()
            stats = {k: round((v / total_scans) * 100) for k, v in stats.items()}
            
        context.update({
            'scan_total': total_scans,
            'scan_stats': stats,
            'recent_scans': scans.order_by('-timestamp')[:3],
            'local_surplus': listings_available.count(),
            'recent_listings': listings_available.order_by('expiry_window')[:5],
        })

    else: # RETAILER or fallback
        context.update({
            'total_batches': Batch.objects.count(),
            'total_listings': listings_available.count(),
            'recent_listings': listings_available.order_by('-created_at')[:5],
        })

    # Ensure is_urgent is set for map markers
    if 'recent_listings' in context:
        recent_list = list(context['recent_listings'])
        for l in recent_list:
            l.is_urgent = l.expiry_window < urgency_threshold
        context['recent_listings'] = recent_list

    return render(request, 'dashboard.html', context)


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
