from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import login, logout
from .views import get_building

app_name = 'building_id'

urlpatterns = [
    path('get/', get_building)
]
