#from django.urls import path
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('minside/', views.booking_overview, name='min side'),
    
    path('room/', views.getRooms, name='search rooms'),
    path('room/<int:roomNr>/booking', views.roombooking, name='roombooking'),

    path('thanks/', views.thanks, name='thanks'),

    #eks: /booking/room/101/
    path('room/<int:roomNr>/', views.room, name='room info'),

    #booking/login gir login siden
    path('login/', views.login_user, name='logg inn'),
    path('logout/', views.logout_user, name='logg ut'),

    #gir registrer siden 
    path('login/booking/signup_test.html', views.signup_user, name="sign up"),

    #booking/roomoverview gir romoversikt siden
    path('roomoverview/', views.roomoverview, name='roomoverview'),

    path('about/', views.about, name='about'),

    # Cleaning information
    path('cleaning/', views.cleaning_index, name='cleaning-index'),
    path('cleaning/lastCleaned', views.cleaning_last_cleaned, name='cleaning-last-cleaned'),
    path('cleaning/clean', views.cleaning_clean, name='cleaning-clean'),
    path('cleaning/<int:NUMBER_OF_DAYS>', views.cleaning, name='cleaning'),

    #test-shit
    #path('signup_test/', views.signup_user, name="signup_test"),
    #path('login_test/', views.login_user, name="login_test")


]



