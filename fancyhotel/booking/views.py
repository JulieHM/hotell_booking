from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from .models import Hotelroom, Booking
from .forms import SearchForm, BookingForm, UserCreateForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from datetime import date, datetime
from django.core.mail import send_mail
from django.conf import settings

from users.models import CustomUser 

from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.response import TemplateResponse
import datetime
from django.contrib import messages


def index(request):
    return render(request, 'booking/index.html')



def thanks(request):
    context = {
        'roomNr' : request.session.get('roomNr'),
        'startDate' : request.session.get('startDate'),
        'endDate' : request.session.get('endDate'),
        }
    email(request)

    return render(request, 'booking/thanks.html', context)


def email(request):
    subject = 'Bookingbekreftelse'
    message = 'Takk for at du booket rom ' + str(request.session.get('roomNr')) + ' den ' + str(request.session.get('startDate')) + ' - ' + str(request.session.get('endDate'))
    email_from = settings.EMAIL_HOST_USER
    try:
        recipient_list = [request.user.email, ]
        send_mail(subject, message, email_from, recipient_list)
    except:
        recipient_list_guest = [request.session['email'], ]
        send_mail(subject, message, email_from, recipient_list_guest)




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
            #global email
            email = request.user.email
            firstName = request.user.first_name
            lastName = request.user.last_name
            phoneNr = request.user.phone_number

            if updated_request['email'] in [None, '']:
                updated_request.update({'email' : email})
            if updated_request['firstName']  in [None, '']:
                updated_request.update({'firstName' : firstName})
            if updated_request['lastName']  in [None, '']:
                updated_request.update({'lastName' : lastName})
            if updated_request['phoneNr']  in [None, '']:
                updated_request.update({'phoneNr' : phoneNr})

        # Create a SearchForm, populate it with data
        form = BookingForm(updated_request)

        # Check if valid
        if form.is_valid():
            # Process data (return Query)
            request.session['roomNr'] = roomNr
            request.session['email'] = form.cleaned_data['email']
            request.session['firstName'] = form.cleaned_data['firstName']
            request.session['lastName'] = form.cleaned_data['lastName']
            request.session['phoneNr'] = form.cleaned_data['phoneNr']

            if request.user.is_authenticated:
                booking = form.save(commit=False)
                booking.customerID = request.user   # Set Booking.CustomerID = logged in user
                booking.save()
            
            else:
                form.save()

                if 'submit_and_register' in request.POST:
                    return HttpResponseRedirect(reverse('sign up'))

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
            form.fields['email'].initial = request.user.email
            form.fields['firstName'].initial = request.user.first_name
            form.fields['lastName'].initial = request.user.last_name
            form.fields['phoneNr'].initial = request.user.phone_number

    
    # At this point, form is either filled-but-invalid or empty. Either way, it can be rendered
    return render(request, 'booking/roombooking.html', {'form': form})



#def login(request):
    #return render(request, 'booking/login.html')



def roomoverview(request):
    return render(request, 'booking/roomoverview.html')



def about(request):
    return render(request, 'booking/about.html')



# Test for å sjekke om bruker er cleaning:
def check_cleaning(user):
    return user.is_cleaner

@login_required()
@user_passes_test(check_cleaning, login_url='', redirect_field_name=None)
def cleaning_index(request):
    return TemplateResponse(request, 'booking/cleaning_index.html')

@login_required()
@user_passes_test(check_cleaning, login_url='', redirect_field_name=None)
def cleaning(request, NUMBER_OF_DAYS):
    """
        A view, rendering an HTML-table with rooms as rows and days as columns

            
        Example of busy_dates, using NUMBER_OF_DAYS = 7:
            busy_dates == {
                101 : [None, None, None, booked, booked, None, None],
                102 : [None, None, booked, None, booked, None, None],
                ...
            }

        An anonymized version of admin.overview
    """

    busy_dates = {}
    header_row_dates = []
    today = datetime.date.today()
    end_of_period = today + datetime.timedelta(NUMBER_OF_DAYS - 1)

    rooms = Hotelroom.objects.all()
    
    # Create header-row
    for i in range(NUMBER_OF_DAYS):
        date = today + datetime.timedelta(i)
        header_row_dates.append(str(date.day) + '/' + str(date.month))

    # Fill busy_dates with NUMBER_OF_DAYS bolean values
    for room in rooms:
        busy_dates[room.roomNumber] = [None] * NUMBER_OF_DAYS

    # Find all bookings in time period:
    bookings = Booking.objects.filter(dateEnd__gte=today).filter(
        Q(dateEnd__lte=end_of_period) | Q(dateStart__lt=end_of_period))

    # Go through bookings, 
    for booking in bookings:
        start_index = (booking.dateStart - today).days
        end_index = (booking.dateEnd - today).days

        if start_index < 0:
            start_index = 0
        if end_index > NUMBER_OF_DAYS:
            end_index = NUMBER_OF_DAYS

        """ Adds a booking to busy_dates. The overview shows each booking starting the day the customer
        arrives, and then have length = as many nights as the customer stays. This means that blank days can always 
        be cleaned after a set checkout-time, while the cleaning the first day of a booking must be done before
        a set checkin-time.
        """
        for i in range(start_index, end_index):
            busy_dates[booking.room.roomNumber][i] = 'booked'

    context = dict(
        # Fill in values here
        header_row_dates = header_row_dates,
        busy_dates = busy_dates,
        weekdays_until_saturday = 6 - today.weekday(),
        weekdays_until_sunday = 7 - today.weekday(),
    )

    return TemplateResponse(request, 'booking/cleaning.html', context)



def room(request, roomNr):
    room = Hotelroom.objects.get(roomNumber=roomNr)
    context = {'room': room,}
    return render(request, 'booking/room.html', context)

def booking_overview(request):
    if request.user.is_authenticated:
        current_user = request.user
        booking = Booking.objects.filter(email = current_user.email)
        personal_info = CustomUser.objects.filter(email = current_user.email)
        context = {
        'info': personal_info,
        'bookings': booking
        }
    else:
        context = {

        }
    return render(request, "booking/minside.html", context)

def getRooms(request):
    """
    Gives a form to search and filter rooms.

    Advanced filtering is inspired by: https://stackoverflow.com/a/16779396
    """
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
            singleBeds = form.cleaned_data['singleBeds']
            includedBreakfast = form.cleaned_data['includedBreakfast']
            includedParking = form.cleaned_data['includedParking']
            includedCancelling = form.cleaned_data['includedCancelling']
            smokingAllowed = form.cleaned_data['smokingAllowed']

            # Set context and session variables to have correct startDate and endDate
            context['startDate'] = startDate
            context['endDate'] = endDate

            request.session['startDate'] = startDate.isoformat()
            request.session['endDate'] = endDate.isoformat()

            rooms = Hotelroom.objects.filter(
                numberOfBeds__gte=minNumberOfBeds).exclude(
                Q(booking__dateEnd__gt=startDate) & Q(booking__dateStart__lt=endDate)).distinct()

            # There must be an easier way to do this...
            if maxPricePrNight != None:
                rooms = rooms.exclude(pricePrNight__gt=maxPricePrNight)
            if singleBeds != None:
                rooms = rooms.exclude(singleBeds__lt=singleBeds)
            if includedBreakfast == True:
                rooms = rooms.filter(includedBreakfast=True)
            if includedParking == True:
                rooms = rooms.filter(includedParking=True)
            if includedCancelling == True:
                rooms = rooms.filter(includedCancelling=True)
            if smokingAllowed == True:
                rooms = rooms.filter(smokingAllowed=True)

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
        # Copy POST request (see comments in roombooking)
        updated_request = request.POST.copy()

        # If values have not been changed and they are initialized to be stored values - insert stored values
        if updated_request.get('email', None) in [None, ''] and request.session.get('email', None) != None:
            updated_request.update({'email' : request.session.get('email')})
        if updated_request.get('first_name', None)  in [None, ''] and request.session.get('first_name', None) != None:
            updated_request.update({'first_name' : request.session.get('firstName')})
        if updated_request.get('last_name', None)  in [None, ''] and request.session.get('last_name', None) != None:
            updated_request.update({'last_name' : request.session.get('lastName')})
        if updated_request.get('phone_number', None)  in [None, ''] and request.session.get('phone_number', None) != None:
            updated_request.update({'phone_number' : request.session.get('phoneNr')})

        form = UserCreateForm(updated_request)
        if form.is_valid():
            form.save()

            #log the user in
            # Get user type
            email = request.POST['email']
            password = request.POST['password1']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # The user actually exists - SHOULD ALWAYS BE TRUE!!!
                login(request, user)
                
                return HttpResponseRedirect(reverse('index'))

            else:
                # SHOULD NEVER HAPPEN!
                raise ValueError('Something went wrong!')
    else:
        form = UserCreateForm()

        # If user information is stored in session - set initial values to be stored values
        if request.session.get('email', None) != None:
            form.fields['email'].initial = request.session.get('email')
        if request.session.get('firstName', None) != None:
            form.fields['first_name'].initial = request.session.get('firstName')
        if request.session.get('lastName', None) != None:
            form.fields['last_name'].initial = request.session.get('lastName')
        if request.session.get('phoneNr', None) != None:
            form.fields['phone_number'].initial = request.session.get('phoneNr')

    return render(request, 'booking/signup_test.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #login the user
            user = form.get_user()
            login(request, user)

            # Get NEXT-value (to redirect):
            valuenext= request.POST.get('next')

            if valuenext == '':
                messages.success(request, "You have successfully logged in")
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.success(request, "You have successfully logged in")
                return HttpResponseRedirect(valuenext)
    else:
        form = AuthenticationForm()

    return render(request, "booking/login_test.html", {'form': form})



def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



