from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # ws paths go here
    path("ws/codeapp/code/", consumers.TestCodeConsumer),
]
