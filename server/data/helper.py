# A method that returns a list of the information for a user
def list_user_info(user):
    user_info = {
            "id": user.user.id,
            "username": user.user.username,
            "email": user.user.email,
            "first_name": user.user.first_name,
            "last_name": user.user.last_name,
            "group": user.user_type,
            "reports": user.reports
    }

    return user_info

# A method that creates a list of users
def create_user_list(users):
    users_list = []

    for user in list(users):
        user_info = list_user_info(user)

        users_list.append(user_info)

    return users_list

# A method that lists a profile's details
def profile_details(profile):
    profile_list = []

    profile_info = {
        "user_id": profile.user.id,
        "user_type": profile.user_type,
    }

    profile_list.append(profile_info)

    return profile_info