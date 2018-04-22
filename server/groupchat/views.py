from django.http import HttpResponse, HttpResponseNotAllowed
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from groupchat.models import Room, Message
from studygroup.models import StudyGroup, StudentsStudyGroups
from groupchat.helper import *

import smtplib

# A view to show the specified study group chat room
def chat_page(request, username, room_id):
    user = User.objects.get(username=username)
    
    return render(request, 'chat_page.html', {'username': user, 'room_number': room_id})

# Links to a page that displays 
def all_groups(request, user_id):
    rooms = Room.objects.all()

    room_details = room_list(rooms)
    
    user = get_object_or_404(User, pk=user_id)

    return render(request, 'group_select.html', {'username': user, 'room_details': room_details})
