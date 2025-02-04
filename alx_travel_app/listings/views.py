

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import os

class PaymentInitiateView(APIView):
    """API view to initiate payment for a booking."""
    
    def post(self, request, booking_id):
        booking = Booking.objects.get(id=booking_id)
        amount = booking.price_per_night  # Assuming the amount is based on the booking price
        
        # Prepare the data for Chapa API
        payment_data = {
            "amount": str(amount),  # Amount should be a string
            "currency": "ETB",  # Change to your desired currency
            "email": request.data.get("email"),  # User's email
            "callback_url": "https://yourcallbackurl.com",  # Replace with your callback URL
            "metadata": {
                "booking_id": booking_id,
            }
        }
        
        # Make a POST request to Chapa API
        response = requests.post(
            "https://api.chapa.co/transaction/initialize",
            json=payment_data,
            headers={"Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}"}
        )
        
        if response.status_code == 200:
            transaction_info = response.json()
            # Create a Payment record
            payment = Payment.objects.create(
                booking=booking,
                amount=amount,
                transaction_id=transaction_info['id'],  # Assuming the transaction ID is in the response
                status='Pending'
            )
            return Response({"payment_id": payment.payment_id, "payment_url": transaction_info['payment_url']}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)

    def verify_payment(self, request, payment_id):
        """API view to verify payment status with Chapa."""
        try:
            payment = Payment.objects.get(payment_id=payment_id)
            response = requests.get(
                f"https://api.chapa.co/transaction/verify/{payment.transaction_id}",
                headers={"Authorization": f"Bearer {os.getenv('CHAPA_SECRET_KEY')}"}
            )
            
            if response.status_code == 200:
                verification_info = response.json()
                # Update payment status based on verification response
                if verification_info['status'] == 'completed':
                    payment.status = 'Completed'
                else:
                    payment.status = 'Failed'
                payment.save()
                
                return Response({"status": payment.status}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import os

class BookingCreateView(APIView):
    """API view to create a booking and initiate payment."""
    
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            # Initiate payment after booking creation
            payment_view = PaymentInitiateView()
            payment_response = payment_view.post(request, booking.id)
            return payment_response  # Return the payment initiation response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
