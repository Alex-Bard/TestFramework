import argparse
import time

from bysnes_logic.Controller import Controller
from bysnes_logic.TestCaseLogStatuses import TestCasLogStatuses
from face.ColorPrint import *
# небольной фреймворк для тестирования. Позволяет писать скрипты для тестированя, запускать их все вместе, или по
# отдельности, позволяет генерировать отчеты запуска тестов в виде html файла.
Написание тестов:

class App(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.init_parser()
        self.controller = Controller()

    def init_parser(self):
        self.parser.add_argument("command", metavar='command', type=str, help="command for test system", choices=['run', 'show_catalog'])
        self.parser.add_argument("-t --tests", metavar='test cases',help="enumeration of test cases", nargs="+")
        self.parser.add_argument("-f --file_name", metavar='name',help="name of report file",  type=str)
        self.args = self.parser.parse_args()

        # print(vars(self.args))
    def command_processing(self):
        input = vars(self.args)
        command = input['command']
        test_cases = input['t __tests']
        # print(test_cases)
        file_name = input['f __file_name']
        if command == "run":
            if test_cases is None:
                if file_name is None:
                    file = open("report.html", "w", encoding='utf-8')
                    self.controller.run_all(file)
                else:
                    file = open(file_name, "w", encoding='utf-8')
                    self.controller.run_all(file)
            else:
                if file_name is None:
                    file = open("report.html", "w", encoding='utf-8')
                else:
                    file = open(file_name, "w", encoding='utf-8')
                for item in test_cases:
                    try:
                        (num_test_scenario, num_test_case) = item.split('.')
                        self.controller.run_test_scenarios_by_number(num_test_scenario, num_test_case)
                        self.controller.calcul_test_scenarios_status(num_test_scenario)
                    except IndexError as e:
                        return
                    except ValueError as e:
                        self.print_log("не верный формат перечисления тест кейсов. Правильно - 'x.y'",
                                       TestCasLogStatuses.danger)
                        return
                self.controller.save_report(file)
                self.controller.print_report()

                # else:
                #     for (num_test_scenario, num_test_case) in test_cases.split('.'):
                #         self.controller.run_test_scenarios_by_number(num_test_scenario, num_test_case)
                #         self.controller.calcul_test_scenarios_status(num_test_scenario)
                #     self.controller.save_report(file)
                #     self.controller.print_report()

        elif command == "show_catalog":
            self.controller.print_test_case_catalog()
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
app = App()
app.command_processing()

# Press the green button in the gutter to run the script.

