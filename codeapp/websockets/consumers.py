from channels.generic.websocket import WebsocketConsumer
import logging
import json

logger = logging.getLogger(__name__)


class TestCodeConsumer(WebsocketConsumer):

    def connect(self):
        logger.error("New connection")

    def receive(self, text_data=None, bytes_data=None):
        # convert json string to python obj
        received_data = json.loads(text_data)
