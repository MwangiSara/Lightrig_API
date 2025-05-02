from django.contrib import admin
from .models import Bookings,Clients,Contact


# Register your models here.
admin.site.register(Bookings)
admin.site.register(Clients)
admin.site.register(Contact)
