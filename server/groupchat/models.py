from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.six import python_2_unicode_compatible

from datetime import datetime

from channels import Group

import json

@python_2_unicode_compatible
class Room(models.Model):
    """
    A room for people to chat in.
    """
    title = models.CharField(max_length=255)
    staff_only = models.BooleanField(default=False)

    def str(self):
        return self.title

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to get sent
        messages as they are generated.
        """
        return Group("room-%s" % self.id)

    def send_message(self, message, user):
        """
        Called to send a message to the room from the user.
        """
        if type(user) is str:
            username = user
        else:
            username = user.username

        final_msg = {'room': str(self.id), 'message': message, 'username': username}

        new_message = Message(room=self, message=message, user=username)

        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )

class Message(models.Model):
    """
    A model for a message sent in a chat room.
    """
    room = models.ForeignKey(Room, on_delete=None)
    user = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True, db_index=True)
