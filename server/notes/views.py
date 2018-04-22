from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from notes.models import StudyGroup
from notes.models import Notes
from notes.helper import *

import json

@api_view(['POST'])
def create_note(request, studygroup_id):
    """
    Creates a new study group note.

    :param request: The request made from the client.
    :param studygroup_id: The id of the study group to create the note for.
    :return: An HttpResponse with code 201 if note was successfully created.
    """
    studygroup = get_object_or_404(StudyGroup, pk=studygroup_id)
    text = json.loads(request.body.decode("utf-8"))['text']

    note = Notes(studygroup=studygroup, text=text)
    note.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_notes(request, studygroup_id):
    """
    Returns all the notes in JSON for a given study group.

    :param request: The request made from the client.
    :param studygroup_id: The id of the study group to return the notes for.
    :return: A JsonResponse with the notes information
    """
    studygroup = get_object_or_404(StudyGroup, pk=studygroup_id)

    notes = Notes.objects.filter(studygroup=studygroup)

    notes_list = notes_info(notes)

    return JsonResponse(notes_list, safe=False)


@api_view(['DELETE'])
def delete_note(request, note_id):
    """
    Removes a study group note.

    :param request: The request made from the client.
    :param note_id: The id of the note to delete.
    :return: An HttpResponse with a response of 200 if the note was successfully deleted.
    """
    note = get_object_or_404(Notes, pk=note_id)
    note.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(['PATCH'])
def edit_note(request, note_id):
    """
    Edits a content of the note.

    :param request: The request made from the client.
    :param note_id: The id of the note to edit.
    :return: An HttpResponse with a response of 200 if the note was successfully edited.
    """
    note = get_object_or_404(Notes, pk=note_id)

    note.text = json.loads(request.body.decode("utf-8"))['text']
    note.save()

    return Response(status=status.HTTP_200_OK)
