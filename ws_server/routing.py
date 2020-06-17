from django.urls import re_path

from ws_server import ws

websocket_urlpatterns = [
    re_path(r'ws/send/$', ws.WebSocketServer),
    # re_path(r'ws/send/$', ws.FrameConsumer),
]
