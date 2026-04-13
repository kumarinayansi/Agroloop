from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import FoodListing, Claim
from .forms import FoodListingForm, ClaimForm


@login_required
def listing_list(request):
    listings = FoodListing.objects.filter(
        status='AVAILABLE',
        expiry_window__gt=timezone.now()
    ).select_related('listed_by').order_by('expiry_window')
    return render(request, 'redistribution/listing_list.html', {'listings': listings})


@login_required
def listing_detail(request, pk):
    listing = get_object_or_404(FoodListing, pk=pk)
    user_claim = None
    if request.user.is_authenticated:
        user_claim = Claim.objects.filter(listing=listing, claimant=request.user).first()
    return render(request, 'redistribution/listing_detail.html', {
        'listing': listing,
        'user_claim': user_claim,
        'claims': listing.claims.select_related('claimant').all(),
    })


@login_required
def listing_create(request):
    if request.method == 'POST':
        form = FoodListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.listed_by = request.user
            listing.save()
            messages.success(request, "Food listing published successfully!")
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = FoodListingForm()
    return render(request, 'redistribution/listing_form.html', {'form': form, 'action': 'Create'})


@login_required
def claim_listing(request, listing_id):
    listing = get_object_or_404(FoodListing, pk=listing_id, status='AVAILABLE')
    if Claim.objects.filter(listing=listing, claimant=request.user).exists():
        messages.warning(request, "You have already submitted a claim for this listing.")
        return redirect('listing_detail', pk=listing_id)

    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.listing = listing
            claim.claimant = request.user
            claim.save()
            messages.success(request, "Your claim has been submitted! The lister will review it.")
            return redirect('listing_detail', pk=listing_id)
    else:
        form = ClaimForm()
    return render(request, 'redistribution/claim_form.html', {'form': form, 'listing': listing})


@login_required
def quick_claim(request, listing_id):
    """Handles a one-click claim from the dashboard or map."""
    if request.method == 'POST':
        listing = get_object_or_404(FoodListing, pk=listing_id, status='AVAILABLE')
        
        if Claim.objects.filter(listing=listing, claimant=request.user).exists():
            messages.warning(request, "You have already claimed this.")
        else:
            Claim.objects.create(
                listing=listing,
                claimant=request.user,
                quantity_requested=listing.quantity, # Default to claiming all for quick claim
                status='PENDING',
                message="Quick claim from dashboard."
            )
            # Log the simulated notification
            print(f"NOTIFICATION: User {request.user.username} claimed {listing.title} from {listing.listed_by.username}")
            messages.success(request, f"Claim submitted for {listing.title}! Notification sent to donor.")
            
        return redirect('dashboard')
    return redirect('listing_list')


@login_required
def my_listings(request):
    listings = FoodListing.objects.filter(listed_by=request.user).order_by('-created_at')
    return render(request, 'redistribution/my_listings.html', {'listings': listings})
