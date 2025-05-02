from django.db import models
from django.contrib.auth.models import User
from accounts.models import Photographer
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.

class Clients(models.Model):
    """
    Represents a client making a booking for videography services.

    Attributes:
        name (CharField): Full name of the client.
        email (EmailField): Client's email address.
        phone_number (CharField): Contact number.
        created_at (DateTimeField): When the client record was created.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
class BookingStatus(models.TextChoices):
    """a custom enumeration for booking statuses in Django using models.TextChoices — a clean and readable way to create choices for a model field
    _() is for translation/localization support (gettext_lazy).
    """

    PENDING = 'P', _('Pending')
    CONFIRMED = 'C', _('Confirmed')
    COMPLETED = 'D', _('Completed')
    CANCELLED = 'X', _('Cancelled')

class Bookings(models.Model):

    """
    Represents a booking made by a client for videography service.

    Attributes:
        client (ForeignKey): The client who made the booking.
        photographer (ForeignKey): The assigned photographer for the booking.
        event_date (DateField): The scheduled date of the event.
        event_time (TimeField): The scheduled time of the event.
        Location (CharField): The location of the event.
        services_type (CharField): The type of service requested (e.g., Wedding Videography, Music Videos).
        booking_status (CharField): The current status of the booking (Pending, Confirmed, etc.).
        project_details (TextField): Additional notes or requirements for the project.
        created_at (DateTimeField): Timestamp when the booking was created.
        updated_at (DateTimeField): Timestamp when the booking was last updated.
    """

    SERVICES_TYPE= (
        ('Wedding Videography','Wedding Videography'),
        ('Commercial Production','Commercial Production'),
        ( 'Music Videos','Music Videos'),
        ('Documentary','Documentary'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Clients,on_delete=models.CASCADE, related_name="booking_details")
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE,related_name="booking_details")
    event_date = models.DateField()
    event_time = models.TimeField()
    Location = models.CharField(max_length=255)
    services_type = models.CharField(max_length=50,choices=SERVICES_TYPE)
    booking_status = models.CharField(max_length=1, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    project_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date', '-event_time']
    
    def __str__(self):
        return f"Booking #{self.id} -  {self.client.name} - {self.event_date}"
    
class Contact(models.Model):
    """"
     Stores contact form submissions from the website or platform.

    This model holds basic inquiry details such as the sender's name, email,
    subject, and message content. It also includes a flag to track whether
    the message has been read.

    Attributes:
        name (CharField): The name of the person sending the message.
        email (EmailField): The sender's email address.
        subject (CharField): The subject line of the message.
        message (TextField): The main content of the inquiry.
        created_at (DateTimeField): Timestamp when the message was submitted.
        is_read (BooleanField): Indicates if the message has been marked as read.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} from {self.name}"


