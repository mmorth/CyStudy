from rest_framework import serializers
from studygroup.models import StudyGroup, StudentsStudyGroups, Courses

# Serializer for the StudentsStudyGroups model
# @author Matthew Orth
class StudentsStudyGroupsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentsStudyGroups
        fields = ('user_id', 'group_id')

# # Serializer for the Courses model
# # @author Matthew Orth
class CoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = ('course_number', 'course_department', 'course_name')

# Serializer for the StudyGroup model
# @author Matthew Orth
class StudyGroupSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = StudyGroup
        fields = ('id', 'course')
