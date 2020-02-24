from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from .models import Hotelroom, Booking
from .forms import SearchForm


def index(request):
    return render(request, 'booking/base.html')

def login(request):
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
                id__in=Booking.objects.exclude(
                Q(dateEnd__lte=startDate)|Q(dateStart__gte=endDate))).distinct()

            if maxPricePrNight != None:
                rooms.exclude(
                pricePrNight__gt=maxPricePrNight)

            return render(request, 'booking/search_result.html', {'rooms': rooms})
            
        # if not valid, return room 404 (for now)
        else:
            return HttpResponseRedirect('/room/404/')
    
    # else (GET or other method) - create blank form
    else:
        form = SearchForm()
        return render(request, 'booking/search.html', {'form': form})



