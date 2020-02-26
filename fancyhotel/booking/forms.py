from django import forms
from .models import Customer, Booking


########################### CUSTOMER ###########################
class CustomerForm(forms.ModelForm):
    """Used for creating new customers"""
    class Meta:
        model = Customer
        fields = '__all__'



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
