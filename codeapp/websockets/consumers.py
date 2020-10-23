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
            if not output['stdout'] and not output['stderr']:
                output['stdout'] = 'Your code not return output'
            self.send_json({'output': output})
        elif content['action'] == 'validate':
            self.send_json({'output': {}})
        else:
            self.send_json({'output': f"ERROR: Invalid action -> {content['action']}"})

    # @classmethod
    # def decode_json(cls, text_data):
    #     return json.loads(text_data, encoding='utf-8')
    #
    # @classmethod
    # def encode_json(cls, content):
    #     return json.dumps(content)
