from channels.generic.websocket import JsonWebsocketConsumer
import logging
from codeapp.tester import runner

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)


class TestCodeConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        logger.debug("New connection")

    def receive_json(self, content, **kwargs):
        logger.debug(content)
        action = content['action']
        if action == 'run':
            output = runner.runcode(content['code'], content['lang'], input=content['input'])
            if not output['stdout'] and not output['stderr']:
                output['stdout'] = 'Your code not return output'
            self.send_json(dict(output=output))
        else:
            self.send_json({'output': f"ERROR: Invalid action -> {content['action']}"})
