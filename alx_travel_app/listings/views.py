# listings/views.py

from rest_framework.viewsets import ModelViewSet
from .models import Booking
from .serializers import BookingSerializer
from .tasks import send_booking_confirmation_email

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        
        # Prepare email details
        user_email = booking.user.email
        booking_details = f"Date: {booking.date}, Service: {booking.service}"
        
        # Trigger Celery task
        send_booking_confirmation_email.delay(user_email, booking_details)
