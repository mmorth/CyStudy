from django.test import TestCase
from studygroup.models import StudyGroup, Courses, StudentsStudyGroups
from calendars.models import Meeting
from data.models import Profile
from django.contrib.auth.models import User
from django.test import Client
from django.shortcuts import render, get_object_or_404
import unittest
import json

# Contains tests for group meetings
# @author Matthew Orth
class CalendarsTests(TestCase):

    def test_create_meeting(self):
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        
        response = c.post('/api/calendar/1/meeting/', json.dumps({"day": 4, "month": 5, "year": 2018, "hour": 10, "minute": 30, "location": "Memorial Union", "description": "End of year meeting."}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Memorial Union')

    def test_update_meeting(self):
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        response = c.post('/api/calendar/1/meeting/', json.dumps({"day": 4, "month": 5, "year": 2018, "hour": 10, "minute": 30, "location": "Memorial Union", "description": "End of year meeting."}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Memorial Union')

        response = c.post('/api/calendar/1/meeting/1/', json.dumps({"day": 14, "month": 9, "year": 2018, "hour": 17, "minute": 10, "location": "Library", "description": "End of year meeting (new location)"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Library')

    def test_delete_meeting(self):
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        response = c.post('/api/calendar/1/meeting/', json.dumps({"day": 4, "month": 5, "year": 2018, "hour": 10, "minute": 30, "location": "Memorial Union", "description": "End of year meeting."}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Memorial Union')

        response = c.post('/api/calendar/1/meeting/delete/', content_type="application/json")
        try:
            Meeting.objects.get(id=1)
            self.fail("Meeting Not Deleted.")
        except:
            pass

    def test_list_meetings(self):
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        response = c.post('/api/calendar/1/meeting/', json.dumps({"day": 4, "month": 5, "year": 2018, "hour": 10, "minute": 30, "location": "Memorial Union", "description": "End of year meeting."}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Memorial Union')
        response = c.post('/api/calendar/1/meeting/', json.dumps({"day": 4, "month": 5, "year": 2018, "hour": 10, "minute": 30, "location": "Memorial Union", "description": "End of year meeting."}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Memorial Union')

        response = c.get('/api/calendar/1/meetings/list/')
        self.assertJSONEqual(response.content, [{"studygroup_id": 1, "meeting_id": 1, "day": 4, "month": 5, "year": 2018, "hour": 10, "minute": 30, "location": "Memorial Union", "description": "End of year meeting."}, {"studygroup_id": 1, "meeting_id": 2, "day": 4, "month": 5, "year": 2018, "hour": 10, "minute": 30, "location": "Memorial Union", "description": "End of year meeting."}])

    def test_show_meeting(self): 
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        response = c.post('/api/calendar/1/meeting/', json.dumps({"day": 4, "month": 5, "year": 2018, "hour": 10, "minute": 30, "location": "Memorial Union", "description": "End of year meeting."}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Memorial Union')
        response = c.post('/api/calendar/1/meeting/', json.dumps({"day": 4, "month": 5, "year": 2018, "hour": 10, "minute": 30, "location": "Memorial Union", "description": "End of year meeting."}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Memorial Union')

        response = c.get('/api/calendar/1/meeting/1/details/')
        self.assertJSONEqual(response.content, [{"studygroup_id": 1, "meeting_id": 1, "day": 4, "month": 5, "year": 2018, "hour": 10, "minute": 30, "location": "Memorial Union", "description": "End of year meeting."}])

