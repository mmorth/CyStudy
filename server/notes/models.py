from django.db import models

from studygroup.models import StudyGroup

# @author Matthew Orth

class Notes(models.Model):
    """
    This class represents a study group note.

    :var studygroup: The note the study group is for.
    :var text: The text the note contains.
    """
    studygroup = models.ForeignKey(StudyGroup, related_name='studygroup_note', on_delete=models.DO_NOTHING, default=None)
    text = models.TextField(default=None)
