from django.db import models
from django.core.validators import MinValueValidator

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

    @property
    def doubleBeds(self):
        return (self.numberOfBeds - self.singleBeds) / 2

    @property
    def floor(self):
        return int(str(self.roomNumber)[0])

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



########################### BOOKING ###########################
class Booking(models.Model):
    room = models.ForeignKey(Hotelroom, on_delete=models.PROTECT)
    customerID = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=40)
    email = models.EmailField()
    phoneNr = models.CharField(max_length=8)
    dateStart = models.DateField(verbose_name="Start date")
    dateEnd = models.DateField(verbose_name="End date")

    class Meta:
        ordering = ['dateStart', 'dateEnd', 'room']

    def __str__(self):
        return F"Room {self.room}: {self.dateStart} - {self.dateEnd}"
