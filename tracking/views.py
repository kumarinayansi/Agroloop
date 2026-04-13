import io
import base64
import qrcode
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.files.base import ContentFile
from .models import Batch, JourneyLog
from .forms import BatchForm, JourneyLogForm


@login_required
def batch_list(request):
    batches = Batch.objects.select_related('farmer').all()
    return render(request, 'tracking/batch_list.html', {'batches': batches})


@login_required
def batch_detail(request, batch_id):
    batch = get_object_or_404(Batch, batch_id=batch_id)
    logs = batch.journey_logs.select_related('logged_by').all()
    return render(request, 'tracking/batch_detail.html', {'batch': batch, 'logs': logs})


@login_required
def batch_create(request):
    if request.method == 'POST':
        form = BatchForm(request.POST, user=request.user)
        if form.is_valid():
            batch = form.save(commit=False)
            batch.farmer = request.user
            batch.save()
            # Auto-generate QR code
            _generate_qr(batch)
            messages.success(request, f"Batch '{batch.crop_name}' created successfully!")
            return redirect('batch_detail', batch_id=batch.batch_id)
    else:
        form = BatchForm(user=request.user)
    return render(request, 'tracking/batch_form.html', {'form': form, 'action': 'Create'})


@login_required
def generate_qr_view(request, batch_id):
    """Returns a QR code PNG for a given batch UUID."""
    batch = get_object_or_404(Batch, batch_id=batch_id)
    qr_url = request.build_absolute_uri(f'/tracking/batch/{batch_id}/')

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#2d6a4f", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')


@login_required
def add_journey_log(request, batch_id):
    batch = get_object_or_404(Batch, batch_id=batch_id)
    if request.method == 'POST':
        form = JourneyLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.batch = batch
            log.logged_by = request.user
            log.save()
            batch.current_status = log.status
            batch.save()
            messages.success(request, "Journey log added.")
            return redirect('batch_detail', batch_id=batch_id)
    else:
        form = JourneyLogForm()
    return render(request, 'tracking/journey_log_form.html', {'form': form, 'batch': batch})


# ── Internal helper ──────────────────────────────────────────────────────────

def _generate_qr(batch):
    """Generates and saves a QR code image on the Batch instance."""
    qr_data = f"AGRIFOODHUB:BATCH:{batch.batch_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#2d6a4f", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    file_name = f"qr_{batch.batch_id}.png"
    batch.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=True)
