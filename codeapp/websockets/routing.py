from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # ws paths go here
    # path("ws/...",consumers.mywsconsumer)
    path("ws/codeapp/code/", consumers.TestCodeConsumer),
    path("ws/codeapp/test/", consumers.TestCodeConsumer)
]
