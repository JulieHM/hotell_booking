from django.contrib import admin
from .models import Hotelroom, Customer, Booking

# Register your models here.

admin.site.register(Hotelroom)
admin.site.register(Customer)
admin.site.register(Booking)