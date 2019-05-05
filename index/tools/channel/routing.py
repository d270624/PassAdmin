from django.urls import path
from index.tools.channel import websocket
from index.tools.channel import websocket_logs
from index.tools.channel import tailf

websocket_urlpatterns = [
    path('webconnect/', websocket.WebSSH),
    path('logs/', websocket_logs.logs),
    path('tailf/', tailf.show),
]
