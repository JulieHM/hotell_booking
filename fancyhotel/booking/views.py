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

            return HttpResponseRedirect(reverse('index'))
    else:
        form = AuthenticationForm()

    return render(request, "booking/login_test.html", {'form': form})



def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
