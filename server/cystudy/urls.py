from django.contrib import admin
from django.conf.urls import include
from django.urls import path
import django_eventstream

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from data import views
from studygroup import views


urlpatterns = [
    path('api/admin/', admin.site.urls, name='admin'),

    path('api/', include('data.urls'), name='data'),
    path('api/studygroup/', include('studygroup.urls'), name='studygroup'),
    path('api/calendar/', include('calendars.urls'), name='calendars'),
    path('api/notes/', include('notes.urls'), name='notes'),
    path('api/groupchat/', include('groupchat.urls'), name='groupchat'),
    path('api/building_id/', include('building_id.urls'), name='building_id'),

    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
]
