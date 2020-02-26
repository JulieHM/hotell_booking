from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from .models import Hotelroom, Booking
from .forms import SearchForm, BookingForm


def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def login(request):
    return render(request, 'login.html')

def thanks(request):
    return HttpResponse('Thanks for booking with Fancy!')

def roombooking(request):
     # If method == POST - process form data
    if request.method == 'POST':

        # Create a SearchForm, populate it with data
        form = BookingForm(request.POST)

        # Check if valid
        if form.is_valid():
            # Process data (return Query)
            booking = Booking()
            booking.room = form.cleaned_data['room']
            booking.firstName = form.cleaned_data['firstName']
            booking.lastName = form.cleaned_data['lastName']
            booking.email = form.cleaned_data['email']
            booking.phoneNr = form.cleaned_data['phoneNr']
            booking.dateStart = form.cleaned_data['dateStart']
            booking.dateEnd = form.cleaned_data['dateEnd']
            booking.save()

            return HttpResponseRedirect(reverse('thanks'))
    
    # else (GET or other method) - create blank form
    else:
        form = BookingForm()
    
    # At this point, form is either filled-but-invalid or empty. Either way, it can be rendered
    return render(request, 'roombooking.html', {'form': form})

def roomoverview(request):
    return render(request, 'roomoverview.html')


def room(request, roomNr):
    return HttpResponse("You are looking at room %s." % roomNr)

def getRooms(request):
    # If method == POST - process form data
    if request.method == 'POST':

        # Create a SearchForm, populate it with data
        form = SearchForm(request.POST)

        # Check if valid
        if form.is_valid():
            # Process data (return Query)
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            minNumberOfBeds = form.cleaned_data['minNumberOfBeds']
            maxPricePrNight = form.cleaned_data['maxPricePrNight']

            rooms = Hotelroom.objects.filter(
                numberOfBeds__gte=minNumberOfBeds).exclude(
                Q(booking__dateEnd__gt=startDate) & Q(booking__dateStart__lt=endDate)).distinct()

            if maxPricePrNight != None:
                rooms.exclude(
                pricePrNight__gt=maxPricePrNight)

            return render(request, 'booking/search_result.html', {'rooms': rooms})
    
    # else (GET or other method) - create blank form
    else:
        form = SearchForm()
    
    return render(request, 'booking/search.html', {'form': form})
