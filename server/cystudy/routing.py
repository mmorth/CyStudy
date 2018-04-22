from channels import route
from groupchat.consumers import ws_connect, ws_disconnect, ws_recieve

channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/(?P<room_number>[0-9]+)$"),
    route("websocket.receive", ws_recieve, path=r"^/(?P<room_number>[0-9]+)$"),
    route("websocket.disconnect", ws_disconnect, path=r"^/(?P<room_number>[0-9]+)$"),
]
