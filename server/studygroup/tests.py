from django.test import TestCase
from .models import StudyGroup, Courses, StudentsStudyGroups
from data.models import Profile
from django.contrib.auth.models import User
from django.test import Client
from django.shortcuts import render, get_object_or_404
import unittest
import json

# Contains tests for study groups
# @author Matthew Orth
class StudyGroupTests(TestCase):

    # -------------------------------- creating, removing, and updating a study group --------------------

    def test_create_study_group(self):
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudyGroup.objects.get(course=1).course.course_name, 'Software Project')
        self.assertEqual(response.content, b'Software Project')

    def test_remove_study_group(self):
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudyGroup.objects.get(course=1).course.course_name, 'Software Project')
        self.assertEqual(response.content, b'Software Project')

        response = c.post('/api/studygroup/1/delete/')
        try:
            StudyGroup.objects.get(id=1)
            self.fail("Studygroup Not Deleted.")
        except:
            pass
    
    def test_update_study_group(self):
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudyGroup.objects.get(course=1).course.course_name, 'Software Project')
        self.assertEqual(response.content, b'Software Project')

        course = Courses(course_number=281, course_department="CPR E", course_name="Digital Logic")
        course.save()

        response = c.post('/api/studygroup/1/update/', json.dumps({"course_id": 2}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudyGroup.objects.get(course=2).course.course_name, 'Digital Logic')
        self.assertEqual(response.content, b'Digital Logic')
        

    # # --------------------------------- joining and leaving a study group -----------------------------------

    def test_join_study_group(self):
        user = User(username='unit99', email='test@example.com', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudyGroup.objects.get(course=1).course.course_name, 'Software Project')
        self.assertEqual(response.content, b'Software Project')

        response = c.post('/api/studygroup/join/', json.dumps({"id": 1, "studygroup_id": 1}), content_type="application/json")
        studentgroup = StudentsStudyGroups.objects.get(user=user, group=StudyGroup.objects.get(id=1))
        self.assertEqual(1, studentgroup.user.id)
        self.assertEqual(1, studentgroup.group.id)

        response = c.post('/api/studygroup/join/', json.dumps({"id": 1, "studygroup_id": 1}), content_type="application/json")
        self.assertEqual(response.content, b'You are already a member of this group.')

    def test_leave_study_group(self):
        user = User(username='unit99', email='test@example.com', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudyGroup.objects.get(course=1).course.course_name, 'Software Project')
        self.assertEqual(response.content, b'Software Project')

        response = c.post('/api/studygroup/join/', json.dumps({"id": 1, "studygroup_id": 1}), content_type="application/json")
        studentgroup = StudentsStudyGroups.objects.get(user=user, group=StudyGroup.objects.get(id=1))
        self.assertEqual(1, studentgroup.user.id)
        self.assertEqual(1, studentgroup.group.id)

        response = c.post('/api/studygroup/1/leave/', json.dumps({"id": 1}), content_type="application/json")
        try:
            StudentsStudyGroups.objects.get(id=1)
            self.fail("Studentgroup Not Deleted.")
        except:
            pass

    # # ---------------------------- listing information about a study group and courses ------------------------------

    def test_show_study_group(self):
        user = User(username='unit99', email='unittest@iastate.edu', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudyGroup.objects.get(course=1).course.course_name, 'Software Project')
        self.assertEqual(response.content, b'Software Project')

        response = c.post('/api/studygroup/join/', json.dumps({"id": 1, "studygroup_id": 1}), content_type="application/json")
        studentgroup = StudentsStudyGroups.objects.get(user=user, group=StudyGroup.objects.get(id=1))
        self.assertEqual(1, studentgroup.user.id)
        self.assertEqual(1, studentgroup.group.id)

        response = c.get('/api/studygroup/show/1/')
        self.assertJSONEqual(response.content, [{"id": 1, "course_department": "COM S", "course_number": 309, "course_name": "Software Project", "members": [{"id": 1, "username": "unit99", "email": "unittest@iastate.edu", "first_name": "Unit", "last_name": "Test"}]}])

    def test_study_group_list(self):
        user = User(username='unit99', email='unittest@iastate.edu', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudyGroup.objects.get(course=1).course.course_name, 'Software Project')
        self.assertEqual(response.content, b'Software Project')

        response = c.post('/api/studygroup/join/', json.dumps({"id": 1, "studygroup_id": 1}), content_type="application/json")
        studentgroup = StudentsStudyGroups.objects.get(user=user, group=StudyGroup.objects.get(id=1))
        self.assertEqual(1, studentgroup.user.id)
        self.assertEqual(1, studentgroup.group.id)

        response = c.get('/api/studygroup/list/')
        self.assertJSONEqual(response.content, [{"id": 1, "course_department": "COM S", "course_number": 309, "course_name": "Software Project", "members": [{"id": 1, "username": "unit99", "email": "unittest@iastate.edu", "first_name": "Unit", "last_name": "Test"}]}])

    def test_student_study_group(self):
        user = User(username='unit99', email='unittest@iastate.edu', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.post('/api/studygroup/create/', json.dumps({"course_id": 1}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudyGroup.objects.get(course=1).course.course_name, 'Software Project')
        self.assertEqual(response.content, b'Software Project')

        response = c.post('/api/studygroup/join/', json.dumps({"id": 1, "studygroup_id": 1}), content_type="application/json")
        studentgroup = StudentsStudyGroups.objects.get(user=user, group=StudyGroup.objects.get(id=1))
        self.assertEqual(1, studentgroup.user.id)
        self.assertEqual(1, studentgroup.group.id)

        response = c.get('/api/studygroup/student/1/studygroups/')
        self.assertJSONEqual(response.content, [{"username": "unit99", "email": "unittest@iastate.edu", "first_name": "Unit", "last_name": "Test"}, {"id": 1, "course_department": "COM S", "course_number": 309, "course_name": "Software Project"}])

    # Update json output format!
    def test_course_list(self):
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.get('/api/studygroup/courses/list/')
        self.assertJSONEqual(response.content, [{"id": 1, "course_department": "COM S", "course_number": 309, "course_name": "Software Project"}])

    def test_show_course(self):
        c = Client()
        course = Courses(course_number=309, course_department="COM S", course_name="Software Project")
        course.save()
        response = c.get('/api/studygroup/show/course/1/')
        self.assertJSONEqual(response.content, [{"id": 1, "course_department": "COM S", "course_number": 309, "course_name": "Software Project"}])


    # # -------------------------------- creating, removing, and updating a course -----------------------------------

    def test_create_course(self):
        c = Client()
        response = c.post('/api/studygroup/course/create/', json.dumps({"course_number": 309, "course_department": "COM S", "course_name": "Software Project"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Courses.objects.get(id=1).course_name, 'Software Project')
        self.assertEqual(response.content, b'Software Project')


    def test_remove_course(self):
        c = Client()
        response = c.post('/api/studygroup/course/create/', json.dumps({"course_number": 309, "course_department": "COM S", "course_name": "Software Project"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Courses.objects.get(id=1).course_name, 'Software Project')
        self.assertEqual(response.content, b'Software Project')

        response = c.post('/api/studygroup/course/1/remove/')
        try:
            Courses.objects.get(id=1)
            self.fail("Course Not Deleted.")
        except:
            pass

    def test_update_course(self):
        c = Client()
        response = c.post('/api/studygroup/course/create/', json.dumps({"course_number": 309, "course_department": "COM S", "course_name": "Software Project"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Courses.objects.get(id=1).course_name, 'Software Project')
        self.assertEqual(response.content, b'Software Project')

        response = c.post('/api/studygroup/course/1/update/', json.dumps({"course_number": 281, "course_department": "CPR E", "course_name": "Digital Logic"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Courses.objects.get(id=1).course_name, 'Digital Logic')
        self.assertEqual(response.content, b'Digital Logic')
