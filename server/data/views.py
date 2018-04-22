from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404

from rest_framework import generics, permissions, renderers, viewsets, status
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse

from data.models import Profile
from data.helper import *

import json

# Responds to the OPTIONS preflight request
# @author John Jago
def options(self, request, *args, **kwargs):
    """
    Responds to the OPTIONS reflight request
    """
    response = http.HttpResponse()
    response['Allow'] = ','.join(['get', 'post', 'put', 'delete', 'options'])
    return response

# ------------------------------ login and logout views -----------------------------------------------------------

# View for login functionality
# This method was modified from: https://docs.djangoproject.com/en/2.0/topics/auth/default/#how-to-log-a-user-in
# @api_view(['POST'])
@csrf_exempt
def login_view(request):
    """
    Provides the login functionality using Django authentication. The username and password are passed in from the client as json.

    :param request: The request made from the client.
    :return: An HttpResponse with either the username or an HttpResponse with status of 401.
    """

    username = json.loads(request.body.decode("utf-8"))['username']
    password = json.loads(request.body.decode("utf-8"))['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        return HttpResponse()
    else:
        return HttpResponse(status=401)

# View for logout functionality
# This method was found at: https://docs.djangoproject.com/en/2.0/topics/auth/default/#how-to-log-a-user-out
@api_view(['POST'])
def logout_view(request):
    """
    Provides the logout functionality using Django authentication.

    :param request: The request made from the client.
    :return: An empty HttpResponse.
    """
    logout(request)

    return HttpResponse()

# ----------------------------------- create, delete, and update user -------------------------------------------------------------------------------------------------------

# View for creating a new user
# @author Matthew Orth
@api_view(['POST'])
def create_user(request):
    """
    Creates a new user. The username, first_name, last_name, email, password, and user_type of the user are passed in from the client as json.

    :param request: The request made from the client.
    :return: An HttpResponse with the username of the user created (used for testing).
    """
    create_username = json.loads(request.body.decode("utf-8"))['username']
    create_first_name = json.loads(request.body.decode("utf-8"))['first_name']
    create_last_name = json.loads(request.body.decode("utf-8"))['last_name']
    create_email = json.loads(request.body.decode("utf-8"))['email']
    create_password = json.loads(request.body.decode("utf-8"))['password']

    new_user = User(username=create_username, first_name=create_first_name, last_name=create_last_name, email=create_email, password=create_password)
    new_user.set_password(new_user.password)

    # user_type = json.loads(request.body.decode("utf-8"))['user_type']

    new_user.save()
    new_profile = Profile(user=new_user, reports=0, user_type=0)
    new_profile.save()

    return HttpResponse(new_user.username)

# View for deleting a existing user
# @author Matthew Orth
@api_view(['DELETE'])
def delete_user(request, id):
    """
    Deletes a specific user with the give id.

    :param request: The request made from the client.
    :param user_id: The id of the user to remove.
    :return: An HttpResponse with the username of the user created (used for testing).
    """

    updated_user = get_object_or_404(User, pk=id)

    updated_user.delete()

    return HttpResponse()

# View to have the student change their information settings
# @author Matthew Orth
@api_view(['POST'])
def change_user_settings(request, user_id):
    """
     Updates information on an existing user. The username, first_name, last_name, email, and password of the user are passed in from the client as json.

    :param request: The request made from the client.
    :param user_id: The id of the user to update informaion about.
    :return: An HttpResponse with the username of the user created (used for testing).
    """
    updated_user = get_object_or_404(User, pk=user_id)
    updated_user.username = json.loads(request.body.decode("utf-8"))['username']
    updated_user.first_name = json.loads(request.body.decode("utf-8"))['first_name']
    updated_user.last_name = json.loads(request.body.decode("utf-8"))['last_name']
    updated_user.email = json.loads(request.body.decode("utf-8"))['email']
    updated_user.password = json.loads(request.body.decode("utf-8"))['password']

    new_user.set_password(new_user.password)
    updated_user.save()

    return HttpResponse(updated_user)

# --------------------------- display information about user's home page and user ---------------------------------------

# View to show a user's home page
# @author Matthew Orth
@api_view(['GET'])
def show_home(request, username):
    """
    Returns in json the user type of the user to determine which home page to display.

    :param request: The request made from the client.
    :param profile_id: The id of the user to show the home page of.
    :return: A JsonResponse of the user_type.
    """

    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    profile_list = profile_details(profile)

    return JsonResponse(profile_list, safe=False)

# View to show information about a user
# @author Matthew Orth
@api_view(['GET'])
def display_user(request, id):
    """
    Returns in json the information about a specific user. It returns the id, username, email, first_name, last_name, group, and reports for a user in json format.

    :param request: The request made from the client.
    :param id: The id of the user to show the information about.
    :return: A JsonResponse of the user information.
    """

    user = get_object_or_404(Profile, pk=id)

    users_list = []

    user_info = list_user_info(user)

    users_list.append(user_info)

    return JsonResponse(users_list, safe=False)

# View to list information about all users
# @author Matthew Orth
@api_view(['GET'])
def list_users(request):
    """
    Returns in json the information about all users. It returns the id, username, email, first_name, last_name, group, and reports for all users in json format.

    :param request: The request made from the client.
    :return: A JsonResponse of the user information.
    """

    users = Profile.objects.all()

    user_list = create_user_list(users)

    return JsonResponse(user_list, safe=False)

# ---------------------------------- Report Users --------------------------

# View to report user
# @author Matthew Orth
@api_view(['POST'])
def report_user(request, id):
    """
    Reports a specific user with a given id.

    :param request: The request made from the client.
    :param user_id: The id of the user to report.
    :return: An HttpResponse with the number of the reports the reported user has (used for testing).
    """
    user = get_object_or_404(Profile, pk=id)
    user.reports += 1
    user.save()

    return HttpResponse(user.reports)
