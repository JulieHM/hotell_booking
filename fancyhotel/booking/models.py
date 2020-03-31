from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.conf import settings
from django.utils import timezone

# Create your models here.

########################### HOTELROOM ###########################
class Hotelroom(models.Model):
    roomNumber = models.IntegerField(unique=True,
                                    validators=[MinValueValidator(101,message="Room number must be three digits (i.e. 101)")])
    numberOfBeds = models.IntegerField()
    pricePrNight = models.IntegerField()
    singleBeds = models.IntegerField(default=0)
    includedBreakfast = models.BooleanField(default = True)
    includedParking = models.BooleanField(default = True)
    includedCancelling = models.BooleanField(default = False)
    smokingAllowed = models.BooleanField(default = False)
    lastCleaned = models.DateTimeField(verbose_name='Last cleaned', default=timezone.now())

    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)

    @property
    def doubleBeds(self):
        return (self.numberOfBeds - self.singleBeds) / 2

    @property
    def floor(self):
        return int(str(self.roomNumber)[0])

    def cleanRoom(self):
        self.lastCleaned = timezone.now()
        self.save()

    class Meta:
        ordering = ['roomNumber']

    def __str__(self):
        return F"{self.roomNumber}"



########################### CUSTOMER ###########################
class Customer(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    phoneNr = models.CharField(max_length=8)

    class Meta:
        ordering = ['lastName', 'firstName']

    def __str__(self):
        return F"{self.lastName},  {self.firstName}"



# ########################### CUSTOM_USER ###########################
# Commented out for now, as I am to tired to implement it properly
# For more information, see comments at forms.UserCreateForm
# class custom_user(models.AbstractBaseUser):
#     first_name = models.CharField(max_length=20)
#     last_name = models.CharField(max_length=40)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=8)

#     USERNAME_FIELD = 'email'
#     EMAIL_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     def is_active(self):
#         return True

#     def get_full_name(self):
#         return __str__(self)

#     def get_short_name(self):
#         return self.first_name

#     class Meta:
#         ordering = ['lastname', 'firstname']
    
#     def __str__(self):
#         return F"{self.last_name}, {self.first_name}"



########################### BOOKING ###########################
class Booking(models.Model):
    room = models.ForeignKey(Hotelroom, on_delete=models.PROTECT)
    customerID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=40)
    email = models.EmailField()
    phoneNr = models.CharField(max_length=8, null=True, blank=True)
    dateStart = models.DateField(verbose_name="Start date")
    dateEnd = models.DateField(verbose_name="End date")

    class Meta:
        ordering = ['dateStart', 'dateEnd', 'room']


    def clean(self):
        """Ensure startDate > endDate
        and that the room has not been booked in the same time period"""

        if self.dateEnd <= self.dateStart:
            raise ValidationError("Start date must be before end date!")
        
        # If there are bookings in the database with:
        # - same room__id
        # - different booking__id
        # - first date at or after dateStart (but before dateEnd)
        # - last date at or before dateEnd (but after dateStart)
        # Raise ValidationError
        if Booking.objects.filter(room__id=self.room_id).exclude(pk=self.pk).filter(
                Q(dateEnd__gt=self.dateStart, dateStart__lt=self.dateEnd)
                ).exists():
            raise ValidationError("Overlapping dates, room has been booked.")


    def __str__(self):
        return F"Room {self.room}: {self.dateStart} - {self.dateEnd}"



########################### BOOKING PROXY ###########################
class BookingOverview(Booking):
    """Proxy of Booking, to use for admin.overview"""
    class Meta:
        proxy = True

    verbose_name = 'Booking Overview'
    verbose_name_plural = 'Booking Overview'