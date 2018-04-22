from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver
from channel.models import LoggedInUser

# A method used to signal that a user has logged in to the websocket
@receiver(user_logged_in)
def on_user_login(sender, **kwargs):
    LoggedInUser.objects.get_or_create(user=kwargs.get('user'))

# A method used to signal that a user has logged out of the websocket
@receiver(user_logged_out)
def on_user_logout(sender, **kwargs):
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()