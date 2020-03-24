from django import forms
from .models import Customer, Booking
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CheckboxDefaultInput(forms.CheckboxInput):
    """
    Override CheckboxInput to have "normal" default values

    Inspired by: https://stackoverflow.com/questions/5190313/django-booleanfield-how-to-set-the-default-value-to-true
    """
    def __init__(self, default=False, *args, **kwargs):
        super(CheckboxDefaultInput, self).__init__(*args, **kwargs)
        self.default = default

    def value_from_datadict(self, data, files, name):
        if name not in data:
            return self.default
        return super(CheckboxDefaultInput, self).value_from_datadict(data, files, name)


########################### CUSTOMER ###########################
# NOT IN USE - CAN BE DELETED?
class CustomerForm(forms.ModelForm):
    """Used for creating new customers"""
    class Meta:
        model = Customer
        fields = '__all__'



########################### USER ###########################
class UserCreateForm(UserCreationForm):
    """Creates an instance of CustomUser"""

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number')



########################### BOOKING ###########################
class BookingForm(forms.ModelForm):
    """Used for creating new bookings"""
    
    class Meta:
        model = Booking
        exclude = ['customerID']

    # Cleaning is done in the class itself (booking.models.Booking)



########################### SEARCH FOR ROOM ###########################
class SearchForm(forms.Form):
    """Used for searching for, and filtering, rooms"""
    startDate = forms.DateField(label='Check in', help_text='Format: yyyy-mm-dd')
    endDate = forms.DateField(label='Check out', help_text='Format: yyyy-mm-dd')
    minNumberOfBeds = forms.IntegerField(label='Number of beds')
    maxPricePrNight = forms.IntegerField(label='Maximum price per night', required=False)

    # Advanced options (hidden by default):
    singleBeds = forms.IntegerField(required=False, label='Number of single beds')
    # floor = forms.IntegerField(required=False, label='Floor')
    includedBreakfast = forms.BooleanField(required=False, label='Breakfast included')
    includedParking = forms.BooleanField(required=False, label='Parking included')
    includedCancelling = forms.BooleanField(required=False, label='Free cancelling included')
    smokingAllowed = forms.BooleanField(required=False, label='Smoking allowed')

    class Meta:
        widgets = {
            'includedBreakfast': CheckboxDefaultInput(default=True, attrs={'id':'includedBreakfast', 'checked': True}),
            'includedParking': CheckboxDefaultInput(default=True, attrs={'id':'includedParking', 'checked': True}),
            'includedCancelling': CheckboxDefaultInput(default=False, attrs={'id':'includedCancelling',}),
            'smokingAllowed': CheckboxDefaultInput(default=False, attrs={'id':'smokingAllowed',}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Ensure startDate is before endDate
        startDate = cleaned_data.get('startDate')
        endDate = cleaned_data.get('endDate')

        if startDate and endDate:
            # Both fields are valid so far
            # Raise error if needed:
            if startDate > endDate:
                raise forms.ValidationError("Check in must be before check out!", code='invalid-date')



class AdvancedSearchForm(SearchForm):
    singleBeds = forms.IntegerField(required=False, label='Number of single beds')
    floor = forms.IntegerField(required=False, label='Floor')
    includedBreakfast = forms.BooleanField(required=False, label='Breakfast included')
    includedParking = forms.BooleanField(required=False, label='Parking included')
    includedCancelling = forms.BooleanField(required=False, label='Free cancelling included')
    smokingAllowed = forms.BooleanField(required=False, label='Smoking allowed')
