#from django.urls import path
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('room/', views.getRooms, name='search rooms'),

    #eks: /booking/room/101/
    path('room/<int:roomNr>/', views.room, name='room info'),

    #booking/login gir login siden
    path('login/', views.login, name='logg inn'),

    #booking/roomoverview gir romoversikt siden
    path('/roomoverview', views.roomoverview, name='roomoverview'),


    path('/about', views.about, name='about'),


]



