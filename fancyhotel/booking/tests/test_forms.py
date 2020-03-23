from django.test import SimpleTestCase
from booking.forms import SearchForm
import datetime
from django.core.exceptions import ValidationError

class TestForms(SimpleTestCase):

    def test_SearchForm_valid_data(self):
        form = SearchForm(data={
            'startDate': datetime.date(2020, 3, 10),
            'endDate': datetime.date(2020, 3, 12),
            'minNumberOfBeds': 2,
            'maxPricePrNight': 1000, 
        })
    
        self.assertTrue(form.is_valid())

    def test_SearchForm_no_data(self):
        form = SearchForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)
    

    #Skulle sjekke om clean fungerer på ønsket måte, men sliter med at super() blir kalt,
    #fordi det ikke finnes noen parent data (tror det er problemet)
    """ def test_SearchForm_invalid_data(self):
        form = SearchForm(data={
            'startDate': datetime.date(2020, 3, 10),
            'endDate': datetime.date(2020, 3, 12),
            'minNumberOfBeds': 2,
            'maxPricePrNight': 1000, 
        })

        self.assertRaises(ValidationError, form.clean) """
