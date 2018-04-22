# A method that returns a list of the information for a meeting
def list_meeting_info(studygroup, meeting):
    data = {
        "studygroup_id": studygroup.id,
        "meeting_id": meeting.id,
        "day": meeting.date_time.day,
        "month": meeting.date_time.month,
        "year": meeting.date_time.year,
        "hour": meeting.date_time.hour,
        "minute": meeting.date_time.minute,
        "location": meeting.location,
        "description": meeting.description
    }

    return data

# A meetings that creates a list of meetings
def meetings_list(meetings, studygroup):
    result = []

    for meeting in list(meetings):
        data = list_meeting_info(studygroup, meeting)

        result.append(data)

    return result
