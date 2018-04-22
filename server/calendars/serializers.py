from rest_framework import serializers
from calendars.models import Schedule

# Serializer for the StudyGroup model
# @author Matthew Orth
class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ('course_id')