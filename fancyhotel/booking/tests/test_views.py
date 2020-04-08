from django.test import TestCase, Client
from django.urls import reverse
from booking.models import Booking, Hotelroom 
import datetime

from django.contrib.auth import authenticate
from users.models import CustomUser

from django.contrib import auth

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.roombooking_url = reverse('roombooking', args=['101'])
        self.thanks_url = reverse('thanks')
        self.booking_overview = reverse('min side')
        self.about = reverse('about')
        self.roomoverview_url = reverse('roomoverview')
        self.room_url = reverse('room info', args=['101'])

        """ Creates 1 hotelroom """
        self.hotelroom_101 = Hotelroom.objects.create(
            id = 1,
            roomNumber= 101,
            numberOfBeds = 2,
            pricePrNight = 500,
            singleBeds = 2
        )
        """ Creates 1 user """
        test_user1 = CustomUser.objects.create(email='Testuser1')
        test_user1.set_password('senha8dg')
        test_user1.save()
        

    def test_index_GET(self):
        response = self.client.get(self.index_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/index.html')
    
    def test_booking_overview(self):
        response = self.client.get(self.booking_overview)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/minside.html')

    def test_about(self):
        response = self.client.get(self.about)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/about.html')

    def test_room(self):
        response = self.client.get(self.room_url)
        self.assertTemplateUsed(response, 'booking/room.html')

    def test_roomoverview(self):
        response = self.client.get(self.roomoverview_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/roomoverview.html')

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

        self.assertEquals(response.status_code, 200)
        self.assertEquals(booking_1.firstName, 'Siw')
        self.assertEquals(booking_1.phoneNr, '90034118')
        self.assertEquals(booking_1.room.roomNumber, 101)
        self.assertTemplateUsed(response, 'booking/thanks.html')


    def test_getRooms_POST(self):
        url = reverse('search rooms')
        response = self.client.post(url, { 
            'startDate': datetime.date(2020, 3, 10),
            'endDate': datetime.date(2020, 3, 12),
            'minNumberOfBeds': 2,
            'maxPricePrNight': 1000, 
        }, follow=True)

        RoomFromResponse = response.context['rooms']
        self.assertQuerysetEqual(RoomFromResponse, Hotelroom.objects.filter(roomNumber = 101), transform=lambda x: x)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/search_result.html')

    def test_signup_POST(self):
        url = reverse('sign up')
        response = self.client.post(url, {
            'email': 'siw_dovle@hotmail.com',
            'password1': 'Hemmelig2',
            'password2': 'Hemmelig2',
            'first_name': 'Siw',
            'last_name': 'Døvle', 
            'phone_number': 90034118
        }, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/index.html')

    
    def test_signup_GET(self):
        url = reverse('sign up')
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/signup_test.html')


    def test_user_login(self):
        url = reverse('logg inn')
        response = self.client.post(url,
                                    {'username': 'Testuser1', 'password': 'senha8dg', 'next': ''}, follow=True)
            
        self.assertTrue(self.client.login(username='Testuser1', password='senha8dg'))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertTemplateUsed(response, 'booking/index.html')

        self.client.logout()

        response = self.client.post(url,
                                    {'username': 'Testuser2', 'password': 'senha8dg'},)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_user_login_next(self):
        url = reverse('logg inn')
        response = self.client.post(url,
                                    {'username': 'Testuser1', 'password': 'senha8dg', 'next': '?next='}, follow=True)
            
        self.assertTrue(self.client.login(username='Testuser1', password='senha8dg'))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertTemplateUsed(response, 'booking/login_test.html')

        self.client.logout()

        response = self.client.post(url,
                                    {'username': 'Testuser2', 'password': 'senha8dg'},)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_user_logout(self):
        url = reverse('logg ut')
        response = self.client.get(url, follow=True)
        self.assertTrue(self.client.login(username='Testuser1', password='senha8dg'))
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertTemplateUsed(response, 'booking/index.html')

        self.client.logout()
        self.assertTrue(user.is_authenticated)

    
        
