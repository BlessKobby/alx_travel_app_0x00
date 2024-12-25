from rest_framework import serializers
from .models import Listing, Booking

class ListingSerializer(serializers.ModelSerializer):
    """Serializer for the Listing model."""
    
    class Meta:
        model = Listing
        fields = ['listing_id', 'title', 'description', 'price_per_night', 'created_at']
        read_only_fields = ['listing_id', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for the Booking model."""
    
    class Meta:
        model = Booking
        fields = ['booking_id', 'listing', 'user', 'start_date', 'end_date', 'created_at']
        read_only_fields = ['booking_id', 'created_at']
