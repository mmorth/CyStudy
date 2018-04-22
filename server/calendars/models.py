from django.db import models
from django.utils import timezone

from datetime import datetime

from studygroup.models import StudyGroup

# Model for a study group meeting
# @author Matthew Orth
class Meeting(models.Model):
    """
    This class represents a study group meeting. 

    :var studygroup: The study group to make the meeting for. This is a foriegn key to the id of the study group to make the meeting for.
    :var date_time: The date and time the meeting will take place.
    :var location: The location of the meeting.
    :var description: The description of the meeting
    """
    studygroup = models.ForeignKey(StudyGroup, related_name='studygroup_meeting', on_delete=models.DO_NOTHING, default=None)
    date_time = models.DateTimeField('Meeting Time', default=None)
    location = models.CharField(max_length=100, default=None)
    description = models.TextField(default=None)
