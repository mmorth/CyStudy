# A method that lists all the rooms
def room_list(rooms):
    room_details = []

    for room in rooms:
        room_details.append(room)

    return room_details

# A method that returns the emails for all members in the study group
def email_list(notification_list):
    emails = []

    for member in notification_list:
        email.append(member.email)

    return emails

# A method that sends an email notification to all members of a studygroup whenever a message is sent
def send_email_notification(room):
    notification_list = StudentsStudyGroups.objects.filter(group=room)

    emails = email_list(notification_list)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    msg = MIMEMultipart()
    msg['From'] = 'cystudyweb@gmail.com'
    msg['To'] = emails
    msg['Subject'] = "CyStudy Notification"
    body = "You have a new CyStudy message."
    msg.attach(MIMEText(body, 'plain'))
    server.login('cystudyweb@gmail.com', "cystudyiowastate")
    server.sendmail('cystudyweb@gmail.com', 'cystudyweb@gmail.com', msg.as_string())
    server.quit()
