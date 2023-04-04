from bysnes_logic.TestScenario import TestScenario
from testCasesExample.TestCase10_1 import *


NAME = "Проверка сетевого взаимодействия"
class TestScenario10(TestScenario):
    def __init__(self):
        self.create_instance_test_cases()

    def create_instance_test_cases(self):
        test_cases = list()
        test_cases.append(TestCase10_1())
        super().__init__(test_cases, NAME)