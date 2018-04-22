import json
from channels import Group, Channel
from channels.auth import channel_session_user, channel_session_user_from_http

import json
from channels import Channel
from channels.auth import channel_session_user_from_http, channel_session_user, channel_session
from datetime import datetime

from groupchat.models import Room, Message
from groupchat.helper import *

from django.shortcuts import get_object_or_404

# A method that is automatically called when a websocket is connected
@channel_session_user_from_http
@channel_session
def ws_connect(message, room_number):
    message.channel_session['rooms'] = []

    room = get_object_or_404(Room, id=room_number)

    prev_messages = room.message_set.all().order_by('date')
    user_messages = {str(message.date): [message.user, message.message] for message in prev_messages}
	
    Group("%s" % message.user).add(message.reply_channel)
    Group("%s" % message.user).send({
        "text": json.dumps({
            "prev_messages": user_messages
        })
    })

    room.send_message('Connected', message.user)

    room.websocket_group.add(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).union([room.id]))
    
# A method that is automatically called when a message is sent/received
@channel_session_user_from_http
@channel_session
def ws_recieve(message, room_number):
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']

    room = get_object_or_404(Room, id=room_number)

    if payload['message'] != '':
        message = Message(user=payload['username'], message=payload['message'], date=datetime.now())
        message.room = room
        message.save()

        room.send_message(payload["message"], payload['username'])

    # This line is used to send an email notification to all members of the chat room
    # that a new message has been sent. This line is left commented out because we have
    # fake users with fake emails
    # send_email_notification(room)

# A method that is automatically called when a websocket is disconnected
@channel_session_user
def ws_disconnect(message, room_number):
    for room_id in message.channel_session.get("rooms", set()):
        try:
            room = Room.objects.get(pk=room_id)
            room.websocket_group.discard(message.reply_channel)
        except Room.DoesNotExist:
            pass
    
    room = get_object_or_404(Room, id=room_number)

    room.send_message('Disconnected', message.user)

    room.websocket_group.discard(message.reply_channel)
    message.channel_session['rooms'] = list(set(message.channel_session['rooms']).difference([room.id]))
