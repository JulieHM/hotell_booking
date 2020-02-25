from django.urls import path

from . import views

urlpatterns = [
<<<<<<< HEAD
    path('home.html', views.home, name="home"),
    path('roomoverview.html', views.roomoverview, name="roomoverview"),
    path('roombooking.html', views.roombooking, name="roombooking"),
    path('login.html', views.login, name="login"),
    path('about.html', views.about, name="about"),
    path('',views.index, name="index"),
] 
=======
    path('', views.index, name='index'),
    
    path('room/', views.getRooms, name='search rooms'),

    #eks: /booking/room/101/
    path('room/<int:roomNr>/', views.room, name='room info'),

]
>>>>>>> master
