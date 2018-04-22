from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    This class represents a user of the cystudy application. This user could be a Student (user_type=0), Moderator (user_type=1), or a Course Admin (user_type=2).

    :var user: The user this profile belongs to. This is a forign key that links to the id of the user the profile is linked to.
    :var reports: The number of reports a user has.
    :var user_type: The type of user. 0 is a Student. 1 is a Moderator. 2 is a Course Admin.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True, default=None)
    reports = models.IntegerField(default=None, blank=True, null=True)
    user_type = models.IntegerField(default=None, blank=True, null=True)
