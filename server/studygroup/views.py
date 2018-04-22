from django.core import serializers
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.models import User, Group

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from data.models import Profile
from studygroup.serializers import StudyGroupSerializer, StudentsStudyGroupsSerializer, CoursesSerializer
from studygroup.models import StudyGroup, StudentsStudyGroups, Courses
from studygroup.helper import *
from groupchat.models import Room, Message

import json


"""
Studygroup views class.
"""

# -------------------------------- creating, removing, and updating a study group --------------------

# View to create a new study group
# @author Matthew Orth
@api_view(['POST'])
def create_study_group(request, username):
    """
    Creates a new, empty study group. The course_id is passed in from the client as json.

    :param request: The request made.
    :return: An HttpResponse with the course name (used for testing).
    """
    create_course_id = json.loads(request.body.decode("utf-8"))['course_id']
    group_course = get_object_or_404(Courses, pk=create_course_id)
    user = User.objects.get(username=username)

    chat_room = Room(title=group_course.course_name)
    chat_room.save()

    new_studygroup = StudyGroup(course=group_course, chat_room=chat_room)
    new_studygroup.save()

    student_group = StudentsStudyGroups(user=user, group=new_studygroup)
    student_group.save()

    return Response(status=status.HTTP_200_OK)

# View to remove a new study group
# @author Matthew Orth
@api_view(['POST'])
def remove_study_group(request, id):
    """
    Removes a study group with the given id.

    :param request: The request made.
    :param id: The id of the study group to delete.
    :return: An empty HttpResponse.
    """
    studygroup = get_object_or_404(StudyGroup, pk=id)
    studygroup.chat_room.delete()
    studygroup.delete()

    return HttpResponse()

# View to update a new study group
# @author Matthew Orth
@api_view(['POST'])
def update_study_group(request, studygroup_id):
    """
    Updates the course for a study group. The new course_id is passed in from the client as json.

    :param request: The request made.
    :param studygroup_id: The id of the study group to update.
    :return: An HttpResponse with the course name (used for testing).
    """
    new_course_id = json.loads(request.body.decode("utf-8"))['course_id']

    new_course = get_object_or_404(Courses, pk=new_course_id)
    studygroup = get_object_or_404(StudyGroup, pk=studygroup_id)

    studygroup.course = new_course
    studygroup.save()

    return HttpResponse(studygroup.course.course_name)

# --------------------------------- joining and leaving a study group -----------------------------------

# View for a stuent to join a new study group
# @author Matthew Orth
@api_view(['POST'])
def join_study_group(request):
    """
    Adds a student to a study group. The username and studygroup_id are passed in from the client as json. Does not allow for the same student to be added to one study group multiple times.

    :param request: The request made.
    :return: An HttpResponse with the study group name or a message stating "You are already a member of this group." if the student is already a member of that study group.
    """
    username = json.loads(request.body.decode("utf-8"))['username']
    user_id = User.objects.get(username=username).id
    studygroup_id = json.loads(request.body.decode("utf-8"))['studygroup_id']

    try:
        StudentsStudyGroups.objects.get(user=user_id, group=studygroup_id) == None
    except:
        user = get_object_or_404(User, pk=user_id)
        studygroup = get_object_or_404(StudyGroup, pk=studygroup_id)
        new_student_study_group = StudentsStudyGroups(user=user, group=studygroup)
        new_student_study_group.save()
        return Response(status=status.HTTP_200_OK)

    return HttpResponse("You are already a member of this group.")

# View for a student to leave a study group
# @author Matthew Orth
@api_view(['POST'])
def leave_study_group(request, studygroup_id):
    """
    Removes a student from a study group. The username of the student is passed in from the client as json.

    :param request: The request made from the client.
    :param studygroup_id: The id of the study group to remove the student from.
    :return: An empty HttpResponse.
    """
    username = json.loads(request.body.decode("utf-8"))['username']
    user_id = User.objects.get(username=username).id
    studygroup = StudentsStudyGroups.objects.get(user_id=user_id, group_id=studygroup_id)
    studygroup.delete()

    return HttpResponse()

# ---------------------------- listing information about a study group and courses ------------------------------

# View to show a study group
# @author Matthew Orth
@api_view(['GET'])
def show_study_group(request, user_id, studygroup_id):
    """
    Returns json information about a specific study group in json format. The study group id, course_department, course_number, course_name, and members id, username, email, first_name, and last_name are returned as json.

    :param request: The request made from the client.
    :param studygroup_id: The id of the study group to display information about.
    :return: A JsonResponse of the information for the study group.
    """
    user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(Profile, pk=user_id)

    studygroup = get_object_or_404(StudyGroup, pk=studygroup_id)
    members = StudentsStudyGroups.objects.filter(group=studygroup_id)

    result = []

    studygroup_data = list_studygroup_info(studygroup=studygroup, members=members, user=profile)

    result.append(studygroup_data)

    return JsonResponse(result, safe=False)


# View to show a specific course
# @author Matthew Orth
@api_view(['GET'])
def show_course(request, course_id):
    """
    Returns json information about a specific course in json format. The course id, course_department, course_number, and course_name are returned in json.

    :param request: The request made from the client.
    :param course_id: The id of the course to display information about.
    :return: A JsonResponse of the information about the course.
    """

    course = Courses.objects.get(id=1)

    result = []

    data = list_course_info(course)

    result.append(data)

    return JsonResponse(result, safe=False)

# View to show all study groups a user is not a member of
# @author Matthew Orth
@api_view(['GET'])
def study_group_not_member(request, username):
    """
    Returns json information about all study groups currently created in json format. The study group id, course_department, course_number, course_name, and members id, username, email, first_name, and last_name are returned as json.

    :param request: The request made from the client.
    :return: A JsonResponse of the information about all study groups.
    """

    id = User.objects.get(username=username).id
    user = get_object_or_404(User, pk=id)
    profile = get_object_or_404(Profile, pk=id)
    member_groups = StudentsStudyGroups.objects.filter(user=id)
    all_study_groups = StudyGroup.objects.all()

    final_list = nomember_groups(member_groups, all_study_groups)

    result = list_multiple_studygroups(final_list, profile)

    return JsonResponse(result, safe=False)

# View to list all studygroups
# @author Matthew Orth
@api_view(['GET'])
def study_group_list(request):
    groups = StudyGroup.objects.all()

    result = list_multiple_studygroups(groups, profile=None)

    return JsonResponse(result, safe=False)

# View to list all courses
# @author Matthew Orth
@api_view(['GET'])
def course_list(request):
    """
    Returns json information about all courses in json format. The course id, course_department, course_number, and course_name are returned in json.

    :param request: The request made from the client.
    :return: A JsonResponse of the information about all courses.
    """

    courses = Courses.objects.all()

    result = list_course(courses)

    return JsonResponse(result, safe=False)

# View to show all study groups a student belongs to
# @author Matthew Orth
@api_view(['GET'])
def student_study_group(request, username):
    """
    Returns json information about all study groups a spcific student is a member of. The study group id, course_department, course_number, course_name, and members id, username, email, first_name, and last_name are returned as json.

    :param request: The request made from the client.
    :param username: The username of the student to display study group information about.
    :return: A JsonResponse of the all study groups a specific user is a member of.
    """
    id = User.objects.get(username=username).id
    user = get_object_or_404(User, pk=id)
    profile = get_object_or_404(Profile, pk=id)
    member_groups = StudentsStudyGroups.objects.filter(user=id)

    member_list = list_members(member_groups)

    result = list_multiple_studygroups(member_list, profile)

    return JsonResponse(result, safe=False)

# -------------------------------- creating, removing, and updating a course -----------------------------------

# View to create a course
# @author Matthew Orth
@api_view(['POST'])
def create_course(request):
    """
    Creates a new course. The course_number, course_department, and course_name are passed in from the client as json.

    :param request: The request made from the client.
    :return: An HttpResponse of the course name (used for testing).
    """
    course_number = json.loads(request.body.decode("utf-8"))['course_number']
    course_department = json.loads(request.body.decode("utf-8"))['course_department']
    course_name = json.loads(request.body.decode("utf-8"))['course_name']

    new_course = Courses(course_number=course_number, course_department=course_department, course_name=course_name)
    new_course.save()

    return Response(status=status.HTTP_200_OK)

# View to remove a course
# @author Matthew Orth
@api_view(['POST'])
def remove_course(request, course_id):
    """
    Removes a course.

    :param request: The request made from the client.
    :param course_id: The id of the course to delete.
    :return: An empty HttpResponse.
    """
    course = get_object_or_404(Courses, pk=course_id)
    course.delete()

    return Response(status=status.HTTP_200_OK)

# View to update a course
# @author Matthew Orth
@api_view(['POST'])
def update_course(request, course_id):
    """
    Updates information about a course. The new course_number, course_department, and course_name are passed in from the client as json.

    :param request: The request made from the client.
    :param course_id: The course id of the course to update.
    :return: An HttpResponse of the course name (used for testing).
    """
    course_number = json.loads(request.body.decode("utf-8"))['course_number']
    course_department = json.loads(request.body.decode("utf-8"))['course_department']
    course_name = json.loads(request.body.decode("utf-8"))['course_name']

    course = get_object_or_404(Courses, pk=course_id)
    course.course_number = course_number
    course.course_department = course_department
    course.course_name = course_name
    course.save()

    return HttpResponse(course.course_name)
