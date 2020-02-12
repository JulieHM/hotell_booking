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
