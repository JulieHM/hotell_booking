from django import forms
from .models import Customer, Booking
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



########################### CUSTOMER ###########################
# NOT IN USE - CAN BE DELETED?
class CustomerForm(forms.ModelForm):
    """Used for creating new customers"""
    class Meta:
        model = Customer
        fields = '__all__'



########################### USER ###########################
class UserCreateForm(UserCreationForm):
    # This form - and the current user - does not, at the moment, register and save phone numbers
    # I'm going to ignore it for now, as it's getting late, but it should probably be looked at later
    # I'm going to keep the model custom_user (only commented out), which may be used for this exact
    # purpose, but I simply do not have the energy to deal with it right now...

    # Inspired by: http://jessenoller.com/blog/2011/12/19/quick-example-of-extending-usercreationform-in-django

    email = forms.EmailField(required = True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=40, required=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')

    def save(self, commit=True):
        """Save User-class. Save field 'email' as 'username'"""
        user = super(UserCreateForm, self).save(commit=False)

        # Store values from userform in model
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user



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
