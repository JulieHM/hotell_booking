from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from .models import Hotelroom, Booking
from .forms import SearchForm, BookingForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from datetime import date, datetime


def index(request):
    return render(request, 'booking/index.html')

def thanks(request):
    return HttpResponse('Thanks for booking with Fancy!')


def roombooking(request, roomNr):
     # If method == POST - process form data
    if request.method == 'POST':
        # request.POST is immutable, so we have to create an updated request in order to add dates
        # For this, I refer to this, which is where I found the recipe:
        # https://stackoverflow.com/questions/18534307/change-a-form-value-before-validation-in-django-form/49296068
        updated_request = request.POST.copy()

        # Set dateStart and dateEnd from session variables (if applicable)
        if request.session.get('startDate', None) != None:
            dateStart = datetime.strptime(request.session['startDate'], "%Y-%m-%d").date()
            updated_request.update({'dateStart' : dateStart})
        if request.session.get('endDate', None) != None:
            dateEnd = datetime.strptime(request.session['endDate'], "%Y-%m-%d").date()
            updated_request.update({'dateEnd' : dateEnd})

        # Create a SearchForm, populate it with data
        form = BookingForm(updated_request)

        # Check if valid
        if form.is_valid():
            # Process data (return Query)

            form.save()

            return HttpResponseRedirect(reverse('thanks'))
    
    # else (GET or other method) - create blank form
    else:
        form = BookingForm()

        if request.session.get('startDate', None) != None:
            form.fields['dateStart'].disabled = True
            dateStart = datetime.strptime(request.session['startDate'], "%Y-%m-%d").date()
            form.fields['dateStart'].initial = dateStart
        if request.session.get('endDate', None) != None:
            form.fields['dateEnd'].disabled = True
            dateEnd = datetime.strptime(request.session['endDate'], "%Y-%m-%d").date()
            form.fields['dateEnd'].initial = dateEnd

    
    # At this point, form is either filled-but-invalid or empty. Either way, it can be rendered
    return render(request, 'booking/roombooking.html', {'form': form})



#def login(request):
    #return render(request, 'booking/login.html')

def roomoverview(request):
    return render(request, 'booking/roomoverview.html')

def about(request):
    return render(request, 'booking/about.html')

def room(request, roomNr):
    room = Hotelroom.objects.get(roomNumber=roomNr)
    context = {'room': room,}
    return render(request, 'booking/room.html', context)

def getRooms(request):
    context = dict()

    # If method == POST - process form data
    if request.method == 'POST':

        # Create a SearchForm, populate it with data
        form = SearchForm(request.POST)
        context['form'] = form

        # Check if valid
        if form.is_valid():
            # Process data (return Query)
            startDate = form.cleaned_data['startDate']
            endDate = form.cleaned_data['endDate']
            minNumberOfBeds = form.cleaned_data['minNumberOfBeds']
            maxPricePrNight = form.cleaned_data['maxPricePrNight']

            # Set context and session variables to have correct startDate and endDate
            context['startDate'] = startDate
            context['endDate'] = endDate

            request.session['startDate'] = startDate.isoformat()
            request.session['endDate'] = endDate.isoformat()

            rooms = Hotelroom.objects.filter(
                numberOfBeds__gte=minNumberOfBeds).exclude(
                Q(booking__dateEnd__gt=startDate) & Q(booking__dateStart__lt=endDate)).distinct()

            if maxPricePrNight != None:
                rooms.exclude(
                pricePrNight__gt=maxPricePrNight)

            context['rooms'] = rooms
            return render(request, 'booking/search_result.html', context)
    
    # else (GET or other method) - create blank form
    else:
        form = SearchForm()

    context['form'] = form

    return render(request, 'booking/search.html', context)

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
