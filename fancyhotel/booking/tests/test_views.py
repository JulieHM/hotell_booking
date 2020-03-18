from django.test import TestCase, Client
from django.urls import reverse
from booking.models import Booking, Hotelroom 
import datetime

""" from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from users.models import CustomUser """

from django.contrib.auth import authenticate

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.roombooking_url = reverse('roombooking', args=['101'])
        self.thanks_url = reverse('thanks')
        self.hotelroom_101 = Hotelroom.objects.create(
            id = 1,
            roomNumber= 101,
            numberOfBeds = 2,
            pricePrNight = 500,
            singleBeds = 2
        )

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/index.html')

    def test_roombooking_GET(self):
        response = self.client.get(self.roombooking_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/roombooking.html')

    def test_roombooking_POST(self):
        url = reverse('roombooking', args=['101'])
        response = self.client.post(url, { 
            'id': 1,
            'room': self.hotelroom_101,
            'firstName': 'Siw',
            'lastName': 'Døvle',
            'email': 'siw_dovle@hotmail.com',
            'phoneNr': 90034118,
            'dateStart': datetime.date(2020, 3, 10),
            'dateEnd': datetime.date(2020, 3, 12)
        }, follow=True)

        booking_1 = Booking.objects.get(email = 'siw_dovle@hotmail.com')
        print(booking_1)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(booking_1.firstName, 'Siw')
        self.assertEquals(booking_1.phoneNr, '90034118')
        self.assertEquals(booking_1.room.roomNumber, 101)
        self.assertTemplateUsed(response, 'booking/thanks.html')


""" class AccountTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        super().setUp()
        user = CustomUser.objects.create(first_name='test', email='test@test.com', is_active=True)
        user.set_password('Test1234')
        user.save()

    def tearDownClass(self):
        self.selenium.quit()
        super().tearDown()

    def test_register(self):
        user = authenticate(username='test', password='Test1234')
        if user is not None: # prints Backend login failed
            print("Backend login successful")
        else:
            print("Backend login failed")

    user = CustomUser.objects.get(username='test')
    print(user)
    print(user.username) # prints test
    print(user.password) # prints Test1234 """

    