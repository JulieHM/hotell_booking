from django.urls import path

from . import views

urlpatterns = [
    path('home.html', views.home, name="home"),
    path('roomoverview.html', views.roomoverview, name="roomoverview"),
    path('roombooking.html', views.roombooking, name="roombooking"),
    path('login.html', views.login, name="login"),
    path('about.html', views.about, name="about"),
    path('',views.index, name="index"),
] 
