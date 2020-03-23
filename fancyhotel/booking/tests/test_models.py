from django.test import TestCase
from booking.models import Booking, Hotelroom
from django.urls import reverse
import datetime
from django.core.exceptions import ValidationError

class TestModels(TestCase):


    def setUp(self):
        self.hotelroom_101 = Hotelroom.objects.create(
            id = 1,
            roomNumber= 101,
            numberOfBeds = 6,
            pricePrNight = 500,
            singleBeds = 2,
        )

        #Fant et problem som kunne oppstått, at det er lov å velge oddeantall senger og partall enkeltsenger
        self.hotelroom_201 = Hotelroom.objects.create(
            id = 2,
            roomNumber= 201,
            numberOfBeds = 5,
            pricePrNight = 500,
            singleBeds = 2,
        )

        self.booking_1 = Booking.objects.create(
            id = 1,
            room = self.hotelroom_101,
            firstName = 'Siw',
            lastName = 'Døvle',
            email = 'siw_dovle@hotmail.com',
            phoneNr = 90034118,
            dateStart = datetime.date(2020, 3, 10),
            dateEnd = datetime.date(2020, 3, 12)
        )

        self.booking_2 = Booking.objects.create(
            id = 2,
            room = self.hotelroom_101,
            firstName = 'Siw',
            lastName = 'Døvle',
            email = 'siw_dovle@hotmail.com',
            phoneNr = 90034118,
            dateStart = datetime.date(2020, 3, 11),
            dateEnd = datetime.date(2020, 3, 13)
        )

        self.booking_3 = Booking.objects.create(
            id = 3,
            room = self.hotelroom_101,
            firstName = 'Siw',
            lastName = 'Døvle',
            email = 'siw_dovle@hotmail.com',
            phoneNr = 90034118,
            dateStart = datetime.date(2020, 3, 5),
            dateEnd = datetime.date(2020, 3, 2)
        )

    #Hotelroom
    def test_hotelroom_dobuleBeds(self):
        self.assertEquals(self.hotelroom_101.doubleBeds, 2)

    def test_hotelroom_dobuleBeds_oddetall(self):
        self.assertEquals(self.hotelroom_201.doubleBeds, 1.5)
    
    def test_hotelroom_floor(self):
        self.assertEquals(self.hotelroom_101.floor, 1)

    #Booking

    def test_booking_exists(self):
        self.assertEquals(self.booking_1.email, 'siw_dovle@hotmail.com') 

    def test_booking_clean_dateStart_before_dateEnd(self):
        self.assertRaises(ValidationError, self.booking_2.clean)

    def test_booking_clean_overlapping(self):
        self.assertRaises(ValidationError, self.booking_3.clean)

    