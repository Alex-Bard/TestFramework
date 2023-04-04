import time
from abc import ABCMeta, abstractmethod, abstractproperty
from bysnes_logic.TestCaseStatuses import TestCaseStatuses

class TestScenario(object):
    def __init__(self, test_cases: list, name: str):
        self.status = None
        self.test_cases = test_cases
        self.executed_test_cases = set(())
        self.name = name
        self.description = ""
        self.is_executed = False

    def get_name(self):
        return self.name
    def get_description(self):
        return self.description

    def get_test_case_name_by_num(self, num:int) -> str:
        return self.test_cases[num].get_name()

    # def get_test_case_description_by_num(self, num:int) -> str:

    def get_count_test_cases(self) -> int:
        return len(self.test_cases)

    def run_all(self):
        for test_case in self.test_cases:
            self.print_log("запускается на исполнение тест кейс '" + test_case.get_name() + "'")
            test_case.execute()
            self.executed_test_cases.add(test_case)
        self.calcul_status()

    def run_by_num(self, num: int):
        self.print_log("запускается на исполнение тест кейс '" + self.test_cases[num].get_name() + "'")
        self.test_cases[num].execute()
        self.executed_test_cases.add(self.test_cases[num])

    @abstractmethod
    def create_instance_test_cases(self):
        """create instance all test cases in this test scenario """

    def get_executed_test_cases(self) -> list:
        return self.executed_test_cases

    def calcul_status(self):
        self.is_executed = True
        status = TestCaseStatuses.passed
        for test_case in self.executed_test_cases:
            if test_case.get_status() is TestCaseStatuses.not_executed:
                status = TestCaseStatuses.not_executed
        for test_case in self.executed_test_cases:
            if test_case.get_status() is TestCaseStatuses.failed:
                status = TestCaseStatuses.failed


        self.status = status

    def get_status(self):
        return self.status

    def print_log(self, text: str):
        print("[" + time.strftime('%H:%M:%S', time.localtime())+ "] " + text)