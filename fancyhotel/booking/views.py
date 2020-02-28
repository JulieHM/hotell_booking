from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from .models import Hotelroom, Booking
from .forms import SearchForm, BookingForm, UserCreateForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from datetime import date, datetime


def index(request):
    return render(request, 'booking/index.html')



def thanks(request):
    context = {
        'roomNr' : request.session.get('roomNr'),
        'startDate' : request.session.get('startDate'),
        'endDate' : request.session.get('endDate'),
        }
    return render(request, 'booking/thanks.html', context)



def roombooking(request, roomNr):
     # If method == POST - process form data
    if request.method == 'POST':
        # request.POST is immutable, so we have to create an updated request in order to add dates
        # For this, I refer to this, which is where I found the recipe:
        # https://stackoverflow.com/questions/18534307/change-a-form-value-before-validation-in-django-form/49296068
        updated_request = request.POST.copy()

        # Set room from URL
        updated_request.update({'room' : Hotelroom.objects.get(roomNumber=roomNr)})

        # Set dateStart and dateEnd from session variables (if applicable)
        if request.session.get('startDate', None) != None:
            dateStart = datetime.strptime(request.session['startDate'], "%Y-%m-%d").date()
            updated_request.update({'dateStart' : dateStart})
        if request.session.get('endDate', None) != None:
            dateEnd = datetime.strptime(request.session['endDate'], "%Y-%m-%d").date()
            updated_request.update({'dateEnd' : dateEnd})

         # Check if name or email has changed. If not, ensure it is user first_ and last_name and email
        if request.user.is_authenticated:
            email = request.user.email
            firstName = request.user.first_name
            lastName = request.user.last_name

            if updated_request['email'] in [None, '']:
                updated_request.update({'email' : email})
            if updated_request['firstName']  in [None, '']:
                updated_request.update({'firstName' : firstName})
            if updated_request['lastName']  in [None, '']:
                updated_request.update({'lastName' : lastName})

        # Create a SearchForm, populate it with data
        form = BookingForm(updated_request)

        # Check if valid
        if form.is_valid():
            # Process data (return Query)

            form.save()
            request.session['roomNr'] = roomNr

            return HttpResponseRedirect(reverse('thanks'))
    
    # else (GET or other method) - create blank form
    else:
        form = BookingForm()

        # Lock room Number
        form.fields['room'].disabled = True
        form.fields['room'].initial = Hotelroom.objects.get(roomNumber=roomNr)

        # Lock dates
        if request.session.get('startDate', None) != None:
            form.fields['dateStart'].disabled = True
            dateStart = datetime.strptime(request.session['startDate'], "%Y-%m-%d").date()
            form.fields['dateStart'].initial = dateStart
        if request.session.get('endDate', None) != None:
            form.fields['dateEnd'].disabled = True
            dateEnd = datetime.strptime(request.session['endDate'], "%Y-%m-%d").date()
            form.fields['dateEnd'].initial = dateEnd

        # If user is logged in / authenticated - populate fields with name and email
        if request.user.is_authenticated:
            form.fields['email'].initial = request.user.username
            form.fields['firstName'].initial = request.user.first_name
            form.fields['lastName'].initial = request.user.last_name

    
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
    """Sign up user, and automatically log in"""
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()

            #log the user in
            # Get user type
            username = request.POST['email']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # The user actually exists - SHOULD ALWAYS BE TRUE!!!
                login(request, user)
                
                return HttpResponseRedirect(reverse('index'))

            else:
                # SHOULD NEVER HAPPEN!
                raise ValueError('Something went wrong!')
    else:
        form = UserCreateForm()

    return render(request, 'booking/signup_test.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #login the user
            user = form.get_user()
            login(request, user)

            return HttpResponseRedirect(reverse('index'))
    else:
        form = AuthenticationForm()

    return render(request, "booking/login_test.html", {'form': form})



def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
