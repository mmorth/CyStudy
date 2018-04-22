from django.db import models
from django.contrib.auth.models import User

from groupchat.models import Room

"""
Studygroup models
"""
# # Model for courses information
# # @author Matthew Orth
class Courses(models.Model):
    """
    This class represents a course.

    :var course_number: The course number of the course.
    :var course_department: The department of the course.
    :var course_name: The name of the course.
    """
    course_number = models.IntegerField(default=None)
    course_department = models.CharField(max_length=100, default=None)
    course_name = models.CharField(max_length=100, default=None)

# Model for study group information
# @author Matthew Orth
class StudyGroup(models.Model):
    """
    This class represents a study group.

    :var course: The course the study group is related to. This is a foriegn key to the course_id of the course the study group is made for.
    :var room: The chat room that the study group has.
    """
    course = models.ForeignKey(Courses, related_name='course', on_delete=models.DO_NOTHING, default=None)
    chat_room = models.ForeignKey(Room, related_name='room', on_delete=models.DO_NOTHING, default=None)

# Model for student and study groups information
# @author Matthew Orth
class StudentsStudyGroups(models.Model):
    """
    This class represents adding a student to a study group

    :var user: The student to add to the study group. This is a foreign key to the user_id to add to the study group.
    :var group: The study group to add the user to. This is a foreign key to the group_id of the study group to add the student to.
    """
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, default=None)
    group = models.ForeignKey(StudyGroup, related_name='group', on_delete=models.CASCADE, default=None)
