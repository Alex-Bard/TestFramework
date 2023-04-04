from bysnes_logic import TestCaseLogStatuses
import time

class TestCaseLog(object):
    def __init__(self, message: str, status: TestCaseLogStatuses):
        self.time = time.localtime()
        self.message = message
        self.status = status

    def get_string(self):
        # return str(self.time) + ": " + self.message + " [" + self.status + "]"
        return time.strftime('%H:%M:%S', self.time) + ": " + self.message