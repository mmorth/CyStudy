from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
from django.test import Client
from django.shortcuts import render, get_object_or_404
import unittest
import json

class DataTests(TestCase):

# ------------------------------ login and logout views -----------------------------------------------------------

    def test_login_view(self):
        user = User(username='unit99', email='test@example.com', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        
        user.id = 99

        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()

        c = Client()
        login_result = c.login(username='unit99', password='unittestpassword')
        self.assertFalse(login_result)

    def test_logout_view(self):
        user = User(username='unit99', email='test@example.com', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        user.id = 99
        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()
        c = Client()
        login_result = c.login(username='not', password='correct')
        self.assertFalse(login_result)

# # ----------------------------------- create, delete, and update user -------------------------------------------------------------------------------------------------------

    def test_create_user(self):
        c = Client()
        response = c.post('/api/account/create/', json.dumps({"username": "unit99", "first_name": "Unit", "last_name": "Test", "email": "unittest@example.com", "password": "unittestpassword", "user_type": 0}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(username="unit99").username, 'unit99')
        self.assertEqual(response.content, b'unit99')

    def test_delete_user(self):
        c = Client()
        response = c.post('/api/account/create/', json.dumps({"username": "unit99", "first_name": "Unit", "last_name": "Test", "email": "unittest@example.com", "password": "unittestpassword", "user_type": 0}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(username="unit99").username, 'unit99')
        self.assertEqual(response.content, b'unit99')
        response = c.post('/api/account/43/delete/')
        try:
            User.objects.get(id=43)
            self.fail("User not deleted.")
        except:
            pass

    def test_change_user_settings(self):
        c = Client()
        response = c.post('/api/account/create/', json.dumps({"username": "unit99", "first_name": "Unit", "last_name": "Test", "email": "unittest@example.com", "password": "unittestpassword", "user_type": 0}), content_type="application/json")
        response = c.post('/api/account/1/settings/', json.dumps({"username": "updateunit", "first_name": "Update", "last_name": "Test", "email": "unittestUpdate@example.com", "password": "unittestupdatepassword"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        updated_user = User.objects.get(id=1)
        updated_profile = Profile.objects.get(user_id=1)
        self.assertEqual(updated_user.username, "updateunit")
        self.assertEqual(updated_user.first_name, "Update")
        self.assertEqual(updated_user.last_name, "Test")
        self.assertEqual(updated_user.email, "unittestUpdate@example.com")
        self.assertEqual(updated_user.password, "unittestupdatepassword")
        self.assertEqual(updated_profile.reports, 0)
        self.assertEqual(updated_profile.user_type, 0)
        

#     # --------------------------- display information about user's home page and user ---------------------------------------

    def test_show_home(self):
        c = Client()
        user = User(username='unit99', email='test@example.com', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()
        response = c.get('/api/user/1/home/')
        self.assertEqual(response.status_code, 200)
        response_content = str(response.content, encoding='utf8')
        self.assertJSONEqual(response_content, [{'user_type': 0}])

        c = Client()
        user = User(username='unit100', email='test@example.com', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 1)
        profile.save()
        response = c.get('/api/user/2/home/')
        self.assertEqual(response.status_code, 200)                
        response_content = str(response.content, encoding='utf8')
        self.assertJSONEqual(response_content, [{'user_type': 1}])

        c = Client()
        user = User(username='unit101', email='test@example.com', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 2)
        profile.save()
        response = c.get('/api/user/3/home/')
        self.assertEqual(response.status_code, 200)
        response_content = str(response.content, encoding='utf8')
        self.assertJSONEqual(response_content, [{'user_type': 2}])

    def test_display_user(self):
        c = Client()
        user = User(username='unit99', email='unittest@example.com', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()
        response = c.get('/api/user/1/display/')
        self.assertEqual(response.status_code, 200)
        response_content = str(response.content, encoding='utf8')
        self.assertJSONEqual(response_content, [{"id": 1, "username": "unit99", "email": "unittest@example.com", "first_name": "Unit", "last_name": "Test", "group": 0, "reports": 0}])

    def test_list_user(self):
        c = Client()
        user = User(username='unit99', email='unittest@iastate.edu', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()
        user = User(username='unit100', email='unittest@iastate.edu', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()
        user = User(username='unit101', email='unittest@iastate.edu', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()
        response = c.get('/api/user/list/')
        self.assertEqual(response.status_code, 200)
        response_content = str(response.content, encoding='utf8')
        self.maxDiff = None
        self.assertJSONEqual(response_content, 
        [{"id": 1, "username": "unit99", "email": "unittest@iastate.edu", "first_name": "Unit", "last_name": "Test", "group": 0, "reports": 0},
        {"id": 2, "username": "unit100", "email": "unittest@iastate.edu", "first_name": "Unit", "last_name": "Test", "group": 0, "reports": 0},
        {"id": 3, "username": "unit101", "email": "unittest@iastate.edu", "first_name": "Unit", "last_name": "Test", "group": 0, "reports": 0}])


#     # ---------------------------------- Report Users --------------------------

    def test_report_user(self):
        c = Client()
        user = User(username='unit99', email='unittest@iastate.edu', password='unittestpassword', first_name="Unit", last_name="Test")
        user.save()
        profile = Profile(user=user, reports=0, user_type = 0)
        profile.save()
        response = c.get('/api/user/1/report/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'1')
