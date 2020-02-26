#from django.urls import path
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('room/', views.getRooms, name='search rooms'),

    path('thanks/', views.thanks, name='thanks'),

    #eks: /booking/room/101/
    path('room/<int:roomNr>/', views.room, name='room info'),

    #booking/login gir login siden
    path('login/', views.login, name='logg inn'),

    #booking/roomoverview gir romoversikt siden
    path('/roomoverview', views.roomoverview, name='roomoverview'),

    path('/about', views.about, name='about'),

    #test-shit
    path('signup_test/', views.signup_user, name="signup_test"),
    path('login_test/', views.login_user, name="login_test")


]



