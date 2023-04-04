from bysnes_logic.TestCaseLogStatuses import TestCasLogStatuses
from bysnes_logic.TestCaseStatuses import TestCaseStatuses
from face.ColorPrint import *


class Report(object):
    MAIN_TEMPLATE_FILE = "face/Templates/MainPage.html"
    TEST_SCENARIO_TEMPLATE_FILE = "face/Templates/TestScenario.html"
    TEST_CASE_TEMPLATE_FILE = "face/Templates/Test_Case.html"
    LOGS_TEMPLATE_FILE = "face/Templates/Logs.html"
    LOG_TEMPLATE_FILE = "face/Templates/Log.html"

    DANGER_BACKGROUND_STYLE = "alert alert-danger"
    WARNING_BACKGROUND_STYLE = "alert alert-warning"
    SUCCESS_BACKGROUND_STYLE = "alert alert-success"

    DANGER_TEXT_STYLE = "text-danger"
    WARNING_TEXT_STYLE = "text-warning"
    SUCCESS_TEXT_STYLE = "text-success"

    def __init__(self, test_scenarios: list):
        self.count_passed_test_cases, self.cont_test_cases = self.calcul_summary(test_scenarios)
        self.test_scenarios = test_scenarios

    def save_report(self, file):
        main_page_template = self.read_file(self.MAIN_TEMPLATE_FILE)
        test_scenario_template = self.read_file(self.TEST_SCENARIO_TEMPLATE_FILE)
        test_case_template = self.read_file(self.TEST_CASE_TEMPLATE_FILE)
        log_plase_template = self.read_file(self.LOGS_TEMPLATE_FILE)
        log_template = self.read_file(self.LOG_TEMPLATE_FILE)

        test_scenarios_replacement_string = ""

        main_page_template = main_page_template.replace("$count_passed_test_cases", str(self.count_passed_test_cases))
        main_page_template = main_page_template.replace("$count_test_cases", str(self.cont_test_cases))
        if self.cont_test_cases == self.count_passed_test_cases:
            main_page_template = main_page_template.replace("$style_count_passed_test_cases",
                                                            self.SUCCESS_BACKGROUND_STYLE)
        else:
            main_page_template = main_page_template.replace("$style_count_passed_test_cases",
                                                            self.DANGER_BACKGROUND_STYLE)
        test_scenarios_replacement_string = self.collect_test_scenarios(test_scenario_template, log_plase_template,
                                                                        test_case_template, log_template)
        main_page_template = main_page_template.replace("$test_scenarios", test_scenarios_replacement_string)

        file.write(main_page_template.encode('utf-8').decode('utf-8'))
        file.close()


    def collect_test_scenarios(self, test_scenario_template, log_plase_template, test_case_template, log_template):
        test_scenarios_replacement_string = ""
        for test_scenario in self.test_scenarios:
            test_scenario_replacement_string = test_scenario_template
            if test_scenario.get_status() is not None:
                test_scenario_replacement_string = test_scenario_replacement_string.replace("$test_scenario_name",
                                                                                            test_scenario.get_name())
                if test_scenario.get_status() is TestCaseStatuses.passed:
                    test_scenario_replacement_string = test_scenario_replacement_string.replace("$style_test_scenario_name",
                                                                                                self.SUCCESS_TEXT_STYLE)
                if test_scenario.get_status() is TestCaseStatuses.failed:
                    test_scenario_replacement_string = test_scenario_replacement_string.replace("$style_test_scenario_name",
                                                                                                self.DANGER_TEXT_STYLE)
                if test_scenario.get_status() is TestCaseStatuses.not_executed:
                    test_scenario_replacement_string = test_scenario_replacement_string.replace("$style_test_scenario_name",
                                                                                                self.WARNING_TEXT_STYLE)

                test_cases_replacement_string = self.collect_test_cases(test_scenario, log_plase_template,
                                                                        test_case_template, log_template)
                test_scenario_replacement_string = test_scenario_replacement_string.replace("$test_case",
                                                                                            test_cases_replacement_string)

                test_scenarios_replacement_string += test_scenario_replacement_string
        return test_scenarios_replacement_string

    def collect_test_cases(self, test_scenario, log_plase_template, test_case_template, log_template) -> str:
        test_cases_replacement_string = ""
        for test_case in test_scenario.get_executed_test_cases():
            log_plase_replacement_string = log_plase_template
            test_case_replacement_string = test_case_template
            if test_case.get_status() is TestCaseStatuses.passed:
                test_case_replacement_string = test_case_replacement_string.replace("$style_test_case_name",
                                                                                    self.SUCCESS_TEXT_STYLE)
                test_case_replacement_string = test_case_replacement_string.replace("$test_case_name",
                                                                                    test_case.get_name() + " [OK]")
            if test_case.get_status() is TestCaseStatuses.failed:
                test_case_replacement_string = test_case_replacement_string.replace("$style_test_case_name",
                                                                                    self.DANGER_TEXT_STYLE)
                test_case_replacement_string = test_case_replacement_string.replace("$test_case_name",
                                                                                    test_case.get_name() + " [FAIL]")
            if test_case.get_status() is TestCaseStatuses.not_executed:
                test_case_replacement_string = test_case_replacement_string.replace("$style_test_case_name",
                                                                                    self.WARNING_TEXT_STYLE)
                test_case_replacement_string = test_case_replacement_string.replace("$test_case_name",
                                                                                    test_case.get_name() +
                                                                                    " [NOT_EXECUTED]")

            if (test_case.get_status() is TestCaseStatuses.failed) or \
                    (test_case.get_status() is TestCaseStatuses.not_executed):

                logs_replacement_string = self.collect_test_case_logs(test_case, log_template)
                log_plase_replacement_string = log_plase_replacement_string.replace("$log", logs_replacement_string)
                test_case_replacement_string = test_case_replacement_string.replace("$logs",
                                                                                    log_plase_replacement_string)
            else:
                test_case_replacement_string = test_case_replacement_string.replace("$logs","")


            test_cases_replacement_string += test_case_replacement_string
        return test_cases_replacement_string

    def collect_test_case_logs(self, test_case, log_template) -> str:
        logs_replacement_string = ""
        for log in test_case.get_logs():
            log_replacement_string = log_template
            log_replacement_string = log_replacement_string.replace("$log_text", log.get_string())
            if log.status is TestCasLogStatuses.danger:
                log_replacement_string = log_replacement_string.replace("$log_style", self.DANGER_TEXT_STYLE)
            elif log.status is TestCasLogStatuses.success:
                log_replacement_string = log_replacement_string.replace("$log_style", self.SUCCESS_TEXT_STYLE)
            elif log.status is TestCasLogStatuses.warning:
                log_replacement_string = log_replacement_string.replace("$log_style", self.WARNING_TEXT_STYLE)
            else:
                log_replacement_string = log_replacement_string.replace("$log_style", "")
            logs_replacement_string += log_replacement_string + "<br>"
        return logs_replacement_string

    def print_report(self):
        self.print_header()
        print("Ткест кейсы:")
        for test_scenario in self.test_scenarios:
            if test_scenario.is_executed:
                if test_scenario.get_status() is TestCaseStatuses.passed:
                    print_green(test_scenario.get_name())
                if test_scenario.get_status() is TestCaseStatuses.failed:
                    print_red(test_scenario.get_name())
                if test_scenario.get_status() is TestCaseStatuses.not_executed:
                    print_yellow(test_scenario.get_name())

                for test_case in test_scenario.get_executed_test_cases():
                    if test_case.get_status() is TestCaseStatuses.passed:
                        print_green("   " + test_case.get_name() + " ... ok")
                    if test_case.get_status() is TestCaseStatuses.failed:
                        print_red("   " + test_case.get_name() + "  ... FAIL")
                    if test_case.get_status() is TestCaseStatuses.not_executed:
                        print_yellow("   " + test_case.get_name() + " ... NOT_EXECUTED")


    def print_header(self):
        print("======================================")
        print("Отчет:")
        print("Тест кейсов успешно пройдено - " + str(self.count_passed_test_cases) +
               " из " + str(self.cont_test_cases))

    def calcul_summary(self, test_scenarios: list) -> (int, int):
        passed = 0
        total = 0
        for test_scenario in test_scenarios:
            for test_case in test_scenario.get_executed_test_cases():
                total += 1
                if test_case.get_status() is TestCaseStatuses.passed:
                    passed += 1

        return passed, total

    def read_file(self, fileName) -> str:
        f = open(fileName, "r", encoding='utf-8')
        content =  f.read()
        f.close()
        return content