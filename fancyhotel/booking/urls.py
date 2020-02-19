from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('room/', views.getRooms, name='search rooms'),

    #eks: /booking/room/101/
    path('room/<int:roomNr>/', views.room, name='room info'),

]
