import time
from bysnes_logic.Report import Report
from bysnes_logic.TestCaseLogStatuses import TestCasLogStatuses
from face.ColorPrint import *
from testScenariesExample.TestScenario10 import TestScenario10

class Controller(object):
    def __init__(self):
        self.test_scenarios = list()
        self.create_instance_all_test_scenarios()


    def create_instance_all_test_scenarios(self) -> list:
        test_scenarios = list()

        test_scenarios.append(TestScenario10())

        self.test_scenarios = test_scenarios

    def print_test_case_catalog(self):
        print("Каталог тест кейсов:")
        for num, test_scenario in enumerate(self.test_scenarios):
            print("Тест сценарий №" + str(num + 1) + ": " + test_scenario.get_name())
            # print(test_scenario.get_name() + "")
            # print(test_scenario.get_description() + "")
            print("Тест кейсы:")
            for num_test_case in range(test_scenario.get_count_test_cases()):
                print("    " + str(num_test_case + 1) + ". "
                      + test_scenario.get_test_case_name_by_num(num_test_case))

    def run_all(self, file):
        for test_scenario in self.test_scenarios:
            self.print_log("запускается на исполнение тест сценарий '" + test_scenario.get_name() + "'")
            test_scenario.run_all()
        report = Report(self.test_scenarios)
        report.print_report()
        report.save_report(file)

    def run_test_scenarios_by_number(self, num_test_scenario:int, num_test_case:int):
        try:
            self.print_log("запускается на исполнение тест сценарий '" +
                           self.test_scenarios[int(num_test_scenario) - 1].get_name()+ "'")
            self.test_scenarios[int(num_test_scenario) - 1].run_by_num(int(num_test_case) - 1)
        except IndexError as e:
            self.print_log("Тест кейса №" + num_test_scenario + "."+ num_test_case + " не существует в системе",
                           TestCasLogStatuses.danger)
            raise e

    def save_report(self, file):
        report = Report(self.test_scenarios)
        report.save_report(file)
    def print_report(self):
        report = Report(self.test_scenarios)
        report.print_report()

    def print_log(self, text: str, status=TestCasLogStatuses.info):
        time_log = time.localtime()
        if status is TestCasLogStatuses.danger:
            print_red("[" + time.strftime('%H:%M:%S', time_log) + "] " + text)
        elif status is TestCasLogStatuses.warning:
            print_yellow("[" + time.strftime('%H:%M:%S', time_log) + "] " + text)
        elif status is TestCasLogStatuses.success:
            print_green("[" + time.strftime('%H:%M:%S', time_log) + "] " + text)
        elif status is TestCasLogStatuses.info:
            print("[" + time.strftime('%H:%M:%S', time_log) + "] " + text)

    def calcul_test_scenarios_status(self,num_test_scenario):
        self.test_scenarios[int(num_test_scenario) - 1].calcul_status()
