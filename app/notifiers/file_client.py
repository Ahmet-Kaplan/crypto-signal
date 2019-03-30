"""Write output to file
"""
import json
import structlog
from datetime import datetime
#from tenacity import retry, retry_if_exception_type, stop_after_attempt

from notifiers.utils import NotifierUtils

class FileNotifier(NotifierUtils):
    """Class for handling file notifications
    """

    def __init__(self,dir='./'):
        """Initialize FileNotifier class
        """
        self.dir = dir

    def notify(self, message):
        """file write the message.

        Args:
            message (str): The message to print.
        """

        message['timestamp'] = str(datetime.utcnow())


        with open(self.dir+'result.json', 'w') as outfile:
            json.dump(message, outfile)

