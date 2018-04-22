from data.helper import list_user_info
from studygroup.models import StudentsStudyGroups

# A method to list the information for a study group
def list_studygroup_info(studygroup, members, user):
    if user:
        list_user_info(user)

    data = {
        "id": studygroup.id,
        "course_department": studygroup.course.course_department,
        "course_number": studygroup.course.course_number,
        "course_name": studygroup.course.course_name
    }

    member_list = []

    for member in list(members):
        group_members = {
            "id": member.user.id,
            "username": member.user.username,
            "email": member.user.email,
            "first_name": member.user.first_name,
            "last_name": member.user.last_name
        }
        member_list.append(group_members)

    data['members'] = member_list

    return data

# A method to list the information of a course
def list_course_info(course):
    data = {
        "id": course.id,
        "course_department": course.course_department,
        "course_number": course.course_number,
        "course_name": course.course_name
    }

    return data

# A method that lists the information about multiple study groups
def list_multiple_studygroups(studygroups, profile):
    result = []

    for studygroup in list(studygroups):
        members = StudentsStudyGroups.objects.filter(group=studygroup.id)

        data = list_studygroup_info(studygroup=studygroup, members=members, user=profile)

        result.append(data)

    return result

# A method that creates a list of study groups a user is not a member of
def nomember_groups(member_groups, all_study_groups):
    member_list = []

    for group in member_groups:
        member_list.append(group.group)

    final_list = []

    for group in all_study_groups:
        if group not in member_list:
            final_list.append(group)

    return final_list

# A method that creates a list of courses
def list_course(courses):
    result = []

    for course in list(courses):
        data = list_course_info(course)

        result.append(data)

    return result

# A method that creates a list of members
def list_members(member_groups):
    member_list = []

    for group in member_groups:
        member_list.append(group.group)

    return member_list