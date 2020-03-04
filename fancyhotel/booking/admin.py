from django.contrib import admin
from .models import Hotelroom, Customer, Booking
from django.contrib.auth.models import Permission



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

    list_display = ('room', 'dateStart', 'dateEnd', 'firstName', 'lastName', 'email')
    list_display_links = ('room', 'firstName', 'lastName')

    list_filter = ('dateStart', 'dateEnd')

    search_fields = ['firstName', 'lastName', 'email']

    permission = ['room', 'dateStart', 'dateEnd']


admin.site.register(Hotelroom)
admin.site.register(Customer)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Permission)

class PermissionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('content_type')
