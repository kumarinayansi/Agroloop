from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from redistribution.models import FoodListing, Claim


class Command(BaseCommand):
    help = 'Seeds demo NGO, Consumer users and sample claims into the database.'

    def handle(self, *args, **options):
        # 1. Create NGO User
        ngo_user, created = CustomUser.objects.get_or_create(
            username='hope_shelter',
            defaults={
                'role': 'NGO',
                'email': 'contact@hopeshelter.org',
                'location': 'Hauz Khas, Delhi',
            }
        )
        if created:
            ngo_user.set_password('password123')
            ngo_user.save()
            self.stdout.write(self.style.SUCCESS('Created NGO user: hope_shelter'))
        else:
            self.stdout.write('NGO user hope_shelter already exists — skipped.')

        # 2. Create Consumer User
        consumer, created = CustomUser.objects.get_or_create(
            username='eco_jane',
            defaults={
                'role': 'CONSUMER',
                'email': 'jane@gmail.com',
                'location': 'Saket, Delhi',
            }
        )
        if created:
            consumer.set_password('password123')
            consumer.save()
            self.stdout.write(self.style.SUCCESS('Created Consumer user: eco_jane'))
        else:
            self.stdout.write('Consumer user eco_jane already exists — skipped.')

        # 3. Create Claims for the NGO
        listings = FoodListing.objects.filter(status='AVAILABLE')[:2]
        for listing in listings:
            Claim.objects.get_or_create(
                listing=listing,
                claimant=ngo_user,
                defaults={
                    'quantity_requested': listing.quantity,
                    'status': 'PENDING',
                    'message': 'We need this for our community kitchen.',
                }
            )
        self.stdout.write(
            self.style.SUCCESS(f'Created claims for NGO on {len(listings)} listing(s).')
        )
