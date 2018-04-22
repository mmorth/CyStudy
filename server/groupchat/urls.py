from django.urls import path
from groupchat import views
from django.contrib import admin
from django.contrib.auth.views import login, logout

app_name = 'groupchat'
urlpatterns = [
    path('accounts/login/', login, name='login'),
    path('accounts/logout/', logout, name='logout'),
    path('<slug:username>/<int:room_id>/chat/', views.chat_page, name='chat_page'),
    path('<int:user_id>/select/', views.all_groups, name='all_groups'),
    path('notify/', views.send_email_notification, name='send_email_notification'),
]
