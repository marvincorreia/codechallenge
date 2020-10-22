from channels.generic.websocket import JsonWebsocketConsumer
import logging
import json
from code_tester import runner

logger = logging.getLogger(__name__)


class TestCodeConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        logger.error("New connection")

    def receive_json(self, content, **kwargs):
        if content['action'] == 'run':
            output = runner.runcode(content['code'], content['lang'])
            self.send_json({'output': output})
        else:
            self.send_json({'output': f"ERROR: Invalid action -> {content['action']}"})
