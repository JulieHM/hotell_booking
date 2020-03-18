from django.test import SimpleTestCase
from django.urls import reverse, resolve
from booking.views import index, thanks, roomoverview, roombooking, signup_user

class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_thanks_url_resolves(self):
        url = reverse('thanks')
        self.assertEquals(resolve(url).func, thanks)

    def test_roombooking_url_resolves(self):
        url = reverse('roombooking', args=['101'])
        self.assertEquals(resolve(url).func, roombooking)
    
    def test_roomoverview_url_resolves(self):
        url = reverse('roomoverview')
        self.assertEquals(resolve(url).func, roomoverview)
    
    def test_signup_user_url_resolves(self):
        url = reverse('sign up')
        self.assertEquals(resolve(url).func, signup_user)
