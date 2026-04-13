import requests as http_requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


OPEN_FOOD_FACTS_URL = "https://en.openfoodfacts.org/api/v2/product/{barcode}.json"

# Health alert thresholds
ALERTS = {
    'sugars_100g': (15, "High Sugar", "This product contains high levels of sugar (>15g/100g)."),
    'saturated-fat_100g': (5, "High Saturated Fat", "Saturated fat exceeds recommended levels (>5g/100g)."),
    'salt_100g': (1.5, "High Salt", "This product has a high sodium/salt content (>1.5g/100g)."),
    'energy-kcal_100g': (400, "High Calorie Density", "Energy dense product (>400 kcal/100g)."),
}


@login_required
def scanner_home(request):
    return render(request, 'nutrition/scanner.html')


from .models import ScanHistory

@login_required
def scan_product(request):
    """Fetches product data from Open Food Facts API using a barcode."""
    barcode = request.GET.get('barcode', '').strip()
    product_name = request.GET.get('product_name', '').strip()
    context = {'barcode': barcode, 'query': product_name}

    if not barcode and not product_name:
        messages.warning(request, "Please enter a valid barcode or product name.")
        return render(request, 'nutrition/scanner.html', context)

    # TEXT SEARCH LOGIC: If user provided a name, find the barcode first
    if product_name and not barcode:
        # Check local common product cache first to bypass external API rate limits/outages
        search_q = product_name.lower().strip()
        common_products = {
            'nutella': '3017620422003',
            'oreo': '7622210449283',
            'coca': '5449000000439',
            'coke': '5449000000439',
            'lays': '0028400199148',
            'pringles': '5053990138722',
            'snickers': '5000159461122',
            'kinder': '8000500037171',
            'red bull': '9002490100070',
            'kitkat': '7613031174953',
            'doritos': '0028400199148'
        }
        
        for key, code in common_products.items():
            if key in search_q:
                barcode = code
                break
                
        if not barcode:
            try:
                # We enforce English globally via the US open food facts api endpoint
                search_url = f"https://us.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&action=process&json=1"
                search_resp = http_requests.get(
                    search_url, 
                    timeout=10, 
                    headers={'User-Agent': 'AgriFoodHub/1.0 (contact@agrifoodhub.com)'}
                )
                search_data = search_resp.json()
                products = search_data.get('products', [])
                
                if search_data.get('count', 0) > 0 and len(products) > 0:
                    # Grab the first matching product's barcode
                    barcode = products[0].get('code', '')
                
                if not barcode:
                    messages.error(request, f"Could not find any English product matching '{product_name}'.")
                    return render(request, 'nutrition/scanner.html', context)
                    
            except Exception as e:
                messages.error(request, f"Text search service is temporarily overloaded. Please try using a barcode instead.")
                return render(request, 'nutrition/scanner.html', context)

    try:
        response = http_requests.get(
            OPEN_FOOD_FACTS_URL.format(barcode=barcode),
            timeout=10,
            headers={'User-Agent': 'AgriFoodHub/1.0 (contact@agrifoodhub.com)'},
        )
        data = response.json()

        if data.get('status') != 1:
            messages.error(request, f"Product with barcode '{barcode}' not found in Open Food Facts database.")
            return render(request, 'nutrition/scanner.html', context)

        product = data['product']
        nutriments = product.get('nutriments', {})
        nutriscore = (product.get('nutriscore_grade') or '').upper()

        # Build health alert list
        health_alerts = []
        has_high_sugar = False
        for key, (threshold, title, description) in ALERTS.items():
            value = nutriments.get(key)
            if value is not None and float(value) > threshold:
                health_alerts.append({'title': title, 'description': description, 'value': round(float(value), 2), 'key': key})
                if key == 'sugars_100g':
                    has_high_sugar = True

        # SAVE TO HISTORY
        ScanHistory.objects.create(
            user=request.user,
            product_name=product.get('product_name_en') or product.get('product_name', 'Unknown'),
            barcode=barcode,
            nutriscore_grade=nutriscore,
            health_alerts_count=len(health_alerts),
            has_high_sugar=has_high_sugar
        )

        context.update({
            'product': {
                'name': product.get('product_name_en') or product.get('product_name', 'Unknown'),
                'brand': product.get('brands', 'N/A'),
                'image_url': product.get('image_url', ''),
                'nutriscore': (product.get('nutriscore_grade') or '').upper(),
                'nova_group': product.get('nova_group', 'N/A'),
                'ingredients': product.get('ingredients_text_en') or product.get('ingredients_text', 'Not available'),
                'categories': product.get('categories_en') or product.get('categories', 'N/A'),
                'quantity': product.get('quantity', 'N/A'),
                'nutriments': {
                    'Energy (kcal)': nutriments.get('energy-kcal_100g', 'N/A'),
                    'Protein (g)': nutriments.get('proteins_100g', 'N/A'),
                    'Carbohydrates (g)': nutriments.get('carbohydrates_100g', 'N/A'),
                    'Sugar (g)': nutriments.get('sugars_100g', 'N/A'),
                    'Fat (g)': nutriments.get('fat_100g', 'N/A'),
                    'Saturated Fat (g)': nutriments.get('saturated-fat_100g', 'N/A'),
                    'Fibre (g)': nutriments.get('fiber_100g', 'N/A'),
                    'Salt (g)': nutriments.get('salt_100g', 'N/A'),
                    'Sodium (g)': nutriments.get('sodium_100g', 'N/A'),
                },
            },
            'health_alerts': health_alerts,
            'alert_count': len(health_alerts),
        })

    except http_requests.Timeout:
        messages.error(request, "The nutrition database timed out. Please try again.")
    except http_requests.RequestException as e:
        messages.error(request, f"Network error: {e}")

    return render(request, 'nutrition/result.html', context)
