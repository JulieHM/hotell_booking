from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from .models import Hotelroom, Booking
from .forms import SearchForm, BookingForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login


def index(request):
    return render(request, 'booking/index.html')

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
            form.save()

            return HttpResponseRedirect(reverse('thanks'))
    
    # else (GET or other method) - create blank form
    else:
        form = BookingForm()
    
    # At this point, form is either filled-but-invalid or empty. Either way, it can be rendered
    return render(request, 'roombooking.html', {'form': form})



def login1(request):
    return render(request, 'booking/login.html')

def roomoverview(request):
    return render(request, 'booking/roomoverview.html')

def about(request):
    return render(request, 'booking/about.html')

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

def signup_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #log the user in
            return HttpResponse("Signed up successfully!")
    else:
        form = UserCreationForm()

    return render(request, 'booking/signup_test.html', {'form': form})

def login_user(request):

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #login the user
            user = form.get_user()
            login(request, user)
            return HttpResponse("Login Successful! Logged in as " + user.get_username())
    else:
        form = AuthenticationForm()

    return render(request, "booking/login_test.html", {'form': form})
