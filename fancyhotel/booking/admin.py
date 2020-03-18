from django.contrib import admin
from .models import Hotelroom, Customer, Booking, BookingOverview
from django.template.response import TemplateResponse
from django.urls import path
from django.db.models import Q
import datetime

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


class BookingOverviewAdmin(admin.ModelAdmin):
    # Disable add-functionality
    def has_add_permission(self, request):
        return False

    # Disable delete-functionality
    def has_delete_permission(self, request, obj=None):
        return False

    # Disable change-functionality
    def has_change_permission(self, request, obj=None):
        return False

    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('', self.admin_site.admin_view(self.overview_index)),
            path('<int:NUMBER_OF_DAYS>', self.admin_site.admin_view(self.overview)),
        ]
        return my_urls + urls

    def overview_index(self, request):
        return TemplateResponse(request, 'admin/overview_index.html')

    def overview(self, request, NUMBER_OF_DAYS):
        """
            A view, rendering an HTML-table with rooms as rows and days as columns

             
            Example of busy_dates, using NUMBER_OF_DAYS = 7:
                busy_dates == {
                    101 : [None, None, None, ['Berg, Andreas', 10], ['Berg, Andreas', 10], None, None]
                    102 : [None, None, ['Nordmann, Ola', 12], None, ['Nordmann, Kari', 13], None, None]
                }
        """

        busy_dates = {}
        header_row_dates = []
        today = datetime.date.today()
        end_of_period = today + datetime.timedelta(NUMBER_OF_DAYS)

        rooms = Hotelroom.objects.all() ##### NEEDED???
        
        # Create header-row
        for i in range(NUMBER_OF_DAYS):
            date = today + datetime.timedelta(i)
            header_row_dates.append(str(date.day) + '/' + str(date.month))

        # Fill busy_dates with NUMBER_OF_DAYS bolean values
        for room in rooms:
            busy_dates[room.roomNumber] = [None] * NUMBER_OF_DAYS

        # Find all bookings in time period:
        bookings = Booking.objects.filter(dateEnd__gte=today).filter(
            Q(dateEnd__lte=end_of_period) | Q(dateStart__lte=end_of_period))

        # Go through bookings, 
        for booking in bookings:
            start_index = (booking.dateStart - today).days
            end_index = (booking.dateEnd - today).days

            if start_index < 0:
                start_index = 0
            if end_index > NUMBER_OF_DAYS:
                end_index = NUMBER_OF_DAYS

            # Loops through start_index + 1 --> end_index, as you might have a booking ending and starting on the same day
            for i in range(start_index + 1, end_index + 1):
                busy_dates[booking.room.roomNumber][i] = dict(
                                            name = (booking.lastName + ', ' + booking.firstName),
                                            id = booking.id)

        context = dict(
            self.admin_site.each_context(request), # Common variables for rendering the admin template
            # Fill in values here
            header_row_dates = header_row_dates,
            busy_dates = busy_dates,
        )

        return TemplateResponse(request, 'admin/overview.html', context)


admin.site.register(Hotelroom)
admin.site.register(Customer)
admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingOverview, BookingOverviewAdmin)