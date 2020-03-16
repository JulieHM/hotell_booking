from django.contrib import admin
from .models import Hotelroom, Customer, Booking

# Register your models here.

class BookingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'room', ('firstName', 'lastName'),
                'email', ('dateStart', 'dateEnd'))}
        ),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                'customerID', 'phoneNr'
            )}
        )
    )

    list_display = ('room', 'dateStart', 'dateEnd', 'firstName', 'lastName', 'email', 'customerID')
    list_display_links = ('room', 'firstName', 'lastName')

    list_filter = ('dateStart', 'dateEnd')

    search_fields = ['firstName', 'lastName', 'email']    


admin.site.register(Hotelroom)
admin.site.register(Customer)
admin.site.register(Booking, BookingAdmin)