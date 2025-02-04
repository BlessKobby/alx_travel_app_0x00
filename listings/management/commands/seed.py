from django.core.management.base import BaseCommand
from listings.models import Listing, Booking, Review

class Command(BaseCommand):
    help = 'Seed the database with sample listings data'

    def handle(self, *args, **kwargs):
        # Create sample listings
        for i in range(1, 6):
            listing = Listing.objects.create(
                title=f'Sample Listing {i}',
                description=f'Description for Sample Listing {i}',
                price_per_night=100 + i * 10
            )
            self.stdout.write(self.style.SUCCESS(f'Created listing: {listing.title}'))

            # Create sample bookings for each listing
            Booking.objects.create(
                listing=listing,
                user=f'user{i}@example.com',
                start_date='2023-01-01',
                end_date='2023-01-05'
            )
            self.stdout.write(self.style.SUCCESS(f'Created booking for: {listing.title}'))

            # Create sample reviews for each listing
            Review.objects.create(
                listing=listing,
                user=f'user{i}@example.com',
                rating=5,
                comment='Great place!'
            )
            self.stdout.write(self.style.SUCCESS(f'Created review for: {listing.title}'))
