import time
from abc import abstractmethod, abstractproperty
from bysnes_logic.TestCaseStatuses import TestCaseStatuses
from bysnes_logic.TestCaseLogStatuses import TestCasLogStatuses
from bysnes_logic.TestCaseLog import TestCaseLog
from face.ColorPrint import *


class TestCase(object):

    def __init__(self, name: str):
        self.status = None
        self.name = name
        self.description = ""
        self.step_logs = list()

        self.db = None

    @abstractmethod
    def run(self):
        """run test case"""

    @abstractmethod
    def before_test(self):
        pass

    @abstractmethod
    def after_test(self):
        pass


    def execute(self):
        log_status = TestCasLogStatuses.warning
        try:
            print("-------------------------------------------------------")
            self.print_log("тест кейс '" + self.name + "' начал исполнение")
            self.print_log("начинается исполнение предварительных условий")
            self.before_test()
        except Exception as e:
            self.print_log("ошибка исполнения предварительных условий тест кейса", TestCasLogStatuses.danger)
            self.print_log("отмена исполнения тест кейса", TestCasLogStatuses.danger)
            self.status = TestCaseStatuses.not_executed
        else:
            self.print_log("предварительные условия были выполнены успешно")
            self.print_log("начинается исполнение основных шагов тест кейса")
            self.run()
        finally:
            self.print_log("начинается откат сисстемы в исходное состояние")
            self.after_test()


        if self.status is TestCaseStatuses.passed:
            log_status = TestCasLogStatuses.success
        elif self.status is TestCaseStatuses.failed:
            log_status = TestCasLogStatuses.danger
        elif self.status is TestCaseStatuses.not_executed:
            log_status = TestCasLogStatuses.warning
        else:
            log_status = TestCasLogStatuses.danger
        self.print_log("тест кейс '" + self.name + "' закончил исполнение со статусом " +
                       self.status.name.upper(), log_status)

    def get_status(self) -> TestCaseStatuses:
        return self.status

    def get_logs(self) -> list:
        return self.step_logs

    def get_name(self):
        return self.name

    def print_log(self, text: str, status=TestCasLogStatuses.info):
        time_log = time.localtime()
        self.step_logs.append(TestCaseLog(text, status))
        if status is TestCasLogStatuses.danger:
            print_red("[" + time.strftime('%H:%M:%S', time_log) + "] " + text)
        elif status is TestCasLogStatuses.warning:
            print_yellow("[" + time.strftime('%H:%M:%S', time_log) + "] " + text)
        elif status is TestCasLogStatuses.success:
            print_green("[" + time.strftime('%H:%M:%S', time_log) + "] " + text)
        elif status is TestCasLogStatuses.info:
            print("[" + time.strftime('%H:%M:%S', time_log) + "] " + text)

    def complete_with_error(self):
        self.status = TestCaseStatuses.failed

    def complete_successfully(self):
        self.status = TestCaseStatuses.passed