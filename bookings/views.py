from django.shortcuts import render
from .serializer import BookingSerializer,ClientSerializer,ContactSerializer
from rest_framework import viewsets, permissions,status,filters
from .models import Bookings,Clients,Contact,Photographer
from django.core.mail import send_mail, EmailMessage
from .permissions import IsOwnerOrReadOnly,IsAuthenticatedOrCreateOnly
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime,timedelta
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.template.loader import render_to_string

# Create your views here.  Define what happens when a user visits a URL (business logic).

class ClientViewset(viewsets.ModelViewSet):
    """
    API endpoint to view or manage clients.
    """
    queryset = Clients.objects.all()
    serializer_class  = ClientSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwnerOrReadOnly] #Only logged-in users (IsAuthenticated) can access the API, And, even if they are logged in: They can edit/delete only their own clients (IsOwnerOrReadOnly). Others' clients: read-only (GET allowed, but no update/delete).

    def perform_create(self, serializer): #erform_create is automatically called by Django when someone POSTs data.
        if self.request.user.is_authenticated:
            return serializer.save(user=self.request.user) #If Sarah is logged in and creates a Client,The Client will have user = Sarah.
        else:
            return serializer.save()
        

    

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint to create bookings along with new client data.
    """
    queryset =  Bookings.objects.all()
    serializer_class  =  BookingSerializer
    permission_classes = [IsAuthenticatedOrCreateOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['booking_status', 'event_date', 'photographer', 'client']
    search_fields = ['event_type', 'location', 'notes']

    def get_queryset(self):
        user = self.request.user
        # only staff to view bookings
        if user.is_staff:
            return Bookings.objects.all()
        
        # Try to get photographer profile
        try:
            photographer = Photographer.objects.get(user=user)
            return Bookings.objects.filter(photographer=photographer)
        except Photographer.DoesNotExist:
            pass
        
        # Try to get client profile
        try:
            client = Clients.objects.get(user=user)
            return Bookings.objects.filter(client=client)
        except Clients.DoesNotExist:
            return Bookings.objects.none()
    def perform_create(self, serializer):
        booking  = serializer.save()
        self._send_booking_notification(booking)

    def perform_update(self, serializer):
        old_status = self.get_object().status
        booking = serializer.save()
        # If status changed, send notification
        if old_status != booking.status:
            self._send_status_update_notification(booking)

    @action(detail=False, methods=['get'])
    def availability(self, request):
        """
            Return a list of event times already booked for a photographer on a given date.
        """
        date_str = request.query_params.get('date')
        photographer_id = request.query_params.get('photographer')

        if not date_str or not photographer_id:
            return Response(
                {"error": "Date and photographer_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            photographer = Photographer.objects.get(id=photographer_id)
        except (ValueError, Photographer.DoesNotExist):
            return Response(
                {"error": "Invalid date format or photographer not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        bookings = Bookings.objects.filter(
            photographer=photographer,
            event_date=date,
            booking_status__in=['P', 'C']  # Adjust field name if needed
        ).order_by('event_time')

        # Just return the booked times
        booked_times = [booking.event_time.strftime('%H:%M') for booking in bookings]

        return Response({'booked_times': booked_times})
        

    def _send_booking_notification(self,booking):
        """Send notification email about new booking"""
        subject=f"Booking Request: {booking.services_type} on {booking.event_date},{booking.event_time}"
        to_email = [booking.photographer.user.email]
        email_message= render_to_string('booking_email.html',{'booking': booking,})
        send_email = EmailMessage(subject=subject,body=email_message,from_email=settings.DEFAULT_FROM_EMAIL,to=to_email)
        send_email.content_subtype='html'
        send_email.send(fail_silently=False)

    def _send_status_update_notification(self, booking):
        """Send notification about booking status update"""
        status_display = booking.get_status_display()
        subject = f"Booking {status_display} - LightRig"
        to_email = booking.client.email

        html_message = render_to_string('emails/booking_email.html', {
            'booking': booking,
            'status_display': status_display
        })

        email = EmailMessage(
            subject,
            html_message,
            settings.DEFAULT_FROM_EMAIL, 
            [to_email],
        )
        email.content_subtype = 'html' 
        email.send()
    

class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint to create contacts
    """
    queryset = Contact.objects.all()
    serializer_class  = ContactSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def perform_create(self, serializer):
        message = serializer.save()
        self._send_contact_notification(message)

    def _send_contact_notification(self,message):
        """Send Admin email about contact information"""
        subject = f"New Contact: {message.subject}"
        email_message = render_to_string('contact_email.html',{'message':message})
        # send to Admin
        admin_email = settings.DEFAULT_FROM_EMAIL
        send_email = EmailMessage(subject=subject,body=email_message,from_email=settings.DEFAULT_FROM_EMAIL,to=[admin_email])
        send_email.content_subtype='html'
        send_email.send(fail_silently=False)
                



