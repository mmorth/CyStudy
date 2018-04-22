from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from calendars.models import Meeting
from studygroup.models import StudyGroup
from calendars.helper import *

import pytz
import json

# View to setup new study group meeting date and time
# @author Matthew Orth
@api_view(['POST'])
def create_group_meeting(request, studygroup_id):
    """
    Creates a new study group meeting for a given study group.

    :param request: The request made from the client.
    :param studygroup_id: The id of the study group to create the new meeting for.
    :return: An HttpResponse with the location of the meeting (used for testing).
    """
    studygroup = get_object_or_404(StudyGroup, pk=studygroup_id)
    day = json.loads(request.body.decode("utf-8"))['day']
    month = json.loads(request.body.decode("utf-8"))['month']
    year = json.loads(request.body.decode("utf-8"))['year']
    hour = json.loads(request.body.decode("utf-8"))['hour']
    minute = json.loads(request.body.decode("utf-8"))['minute']
    location = json.loads(request.body.decode("utf-8"))['location']
    description = json.loads(request.body.decode("utf-8"))['description']

    new_meeting = Meeting(studygroup=studygroup, location=location, description=description, date_time=timezone.now())
    new_meeting.date_time = datetime(year, month, day, hour, minute, tzinfo=pytz.UTC)
    new_meeting.save()

    return Response(status=status.HTTP_201_CREATED)

# View to edit a existing group meeting
# @author Matthew Orth
@api_view(['POST'])
def edit_group_meeting(request, studygroup_id, meeting_id):
    """
    Updates a study group meeting for a given study group.

    :param request: The request made from the client.
    :param studygroup_id: The id of the study group to update the meeting for.
    :param meeting_id: The id of the meeting to update.
    :return: An HttpResponse with the location of the meeting (used for testing).
    """
    studygroup = get_object_or_404(StudyGroup, pk=studygroup_id)
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    day = json.loads(request.body.decode("utf-8"))['day']
    month = json.loads(request.body.decode("utf-8"))['month']
    year = json.loads(request.body.decode("utf-8"))['year']
    hour = json.loads(request.body.decode("utf-8"))['hour']
    minute = json.loads(request.body.decode("utf-8"))['minute']
    meeting.location = json.loads(request.body.decode("utf-8"))['location']
    meeting.description = json.loads(request.body.decode("utf-8"))['description']

    meeting.date_time = datetime(year, month, day, hour, minute, tzinfo=pytz.UTC)
    meeting.save()

    return HttpResponse(meeting.location)

# # View to delete an existing group meeting
# @author Matthew Orth
@api_view(['DELETE'])
def delete_group_meeting(request, studygroup_id, meeting_id):
    """
    Deletes a study group meeting for a given study group.

    :param request: The request made from the client.
    :param studygroup_id: The id of the study group to delete a meeting for.
    :param meeting_id: The id of the meeting to remove.
    :return: An empty HttpResponse.
    """
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    meeting.delete()

    return HttpResponse()

# # View to display a specific group meeting
# @author Matthew Orth
@api_view(['GET'])
def show_group_meeting(request, studygroup_id, meeting_id):
    """
    Returns as json the details of a specific meeting. The studygroup_id, meeting_id, day, month, year, hour, minute, location, and description of the meeting are returned as json.

    :param request: The request made from the client.
    :param studygroup_id: The id of the study group to list a meeting for.
    :param meeting_id: The id of the meeting to display.
    :return: A JsonReponse with the information about a specific meeting.
    """

    studygroup = get_object_or_404(StudyGroup, pk=studygroup_id)
    meeting = get_object_or_404(Meeting, pk=meeting_id)

    result = []

    data = list_meeting_info(studygroup, meeting)

    result.append(data)

    return JsonResponse(result, safe=False)

# # View to display all group meetings for a study group
# @author Matthew Orth
@api_view(['GET'])
def list_group_meetings(request, studygroup_id):
    """
    Returns as json the details of all meetings. The studygroup_id, meeting_id, day, month, year, hour, minute, location, and description for all meetings are returned as json.

    :param request: The request made from the client.
    :param studygroup_id: The id of the study group to delete a meeting for.
    :return: A JsonReponse with the information about a specific meeting.
    """
    studygroup = get_object_or_404(StudyGroup, pk=studygroup_id)

    meetings = Meeting.objects.filter(studygroup=studygroup)

    result = meetings_list(meetings, studygroup)

    return JsonResponse(result, safe=False)
