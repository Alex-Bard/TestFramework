import os
import platform
import subprocess

from bysnes_logic.TestCase import TestCase
from bysnes_logic.TestCaseStatuses import TestCaseStatuses
from bysnes_logic.TestCaseLog import TestCaseLog
from bysnes_logic.TestCaseLogStatuses import TestCasLogStatuses

NAME = "Проверка возможности сетевого подключения к веб приложению"
class TestCase10_1(TestCase):

    def __init__(self):
        super().__init__(NAME)

    def run(self):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', "192.168.19.128"]
        self.print_log("отправка ping запроса на адрес '192.168.19.128'")
        if subprocess.call(command) == 0:
            self.print_log("ping запрос прошел успешно")
            self.status = TestCaseStatuses.passed
        else:
            self.print_log("ping запрос прошел неуспешно", TestCasLogStatuses.danger)
            self.status = TestCaseStatuses.failed
    def after_test(self):
        pass