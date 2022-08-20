from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('', views.index, name='index'),
   path('<str:room_name>/', views.room),
]
