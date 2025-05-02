from rest_framework import serializers
from .models import Bookings,Clients,Photographer,Contact
from datetime import date

# creates classes that takes our model objects and makes it a json data, its more of like the modelForm

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ['id', 'name', 'email', 'phone_number', 'created_at']
        read_only_fields = ['id', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(write_only=True)
    client_email = serializers.EmailField(write_only=True)
    client_phone = serializers.CharField(write_only=True)
    status_display = serializers.CharField(source='get_booking_status_display', read_only=True) # Django automatically adds a method called get_FIELDNAME_display() to the model instance.
    photographer = serializers.PrimaryKeyRelatedField(queryset=Photographer.objects.all(), write_only=True)  #  Accept photographer ID during POST
    photographer_name = serializers.ReadOnlyField(source='photographer.user.get_full_name') # only for GET/display

    class Meta: 
        model = Bookings
        fields = ['id','client_name','client_email','client_phone','photographer','photographer_name', 'event_date','event_time','Location', 'services_type', 'project_details','status_display']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        """ check if photographer is available """
        event_date = attrs.get('event_date')
        photographer_det = attrs.get('photographer_name')
        if event_date <  date.today():
            raise serializers.ValidationError("Event date cannot be in the past.")
        
        # Find all pending or confirmed bookings on the same date, by the same photographer, excluding the one we're currently updating (if any).
        overlapping_booking = Bookings.objects.filter(
            photographer = photographer_det,
            event_date = attrs['event_date'],
            booking_status__in=['P','C'] ,
        ).exclude(pk=self.instance.pk if self.instance else None)

        for booking in overlapping_booking:
            if attrs['event_time'] == booking.event_time:
                raise serializers.ValidationError(
                    "The photographer is already booked during this time slot."
                )
        return attrs
    def create(self, validated_data):
        # Extract client data
        client_name = validated_data.pop('client_name')
        client_email = validated_data.pop('client_email')
        client_phone = validated_data.pop('client_phone')

        # Create or get client instance
        client, created = Clients.objects.get_or_create(
        email=client_email, phone_number=client_phone,
        defaults={'name': client_name, 'phone_number': client_phone})

        # Create the booking with the client FK
        booking = Bookings.objects.create(client=client, **validated_data)
        return booking

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields=  ['id', 'name', 'email', 'subject', 'message', 'created_at', 'is_read']
        read_only_fields =['id', 'is_read', 'created_at']