from rest_framework import serializers
from data.models import *

# Serializer for the Notes model
# @author Matthew Orth
class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notes
        fields = ('filepath', 'group_id')