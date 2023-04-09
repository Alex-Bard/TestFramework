# Simple test framework

### This is a simple test framework that allows you to write test scripts and run them either individually or together. It also allows you to generate an HTML report.
## Installation

First, clone the repository:
```commandline
git clone https://github.com/Alex-Bard/TestFramework.git
```
Move to the project folder:
```commandline
cd .\TestFramework\
```
Download dependencies:
```commandline
pip install -r requirements.txt
```
## Usage

There are two commands:
- `show_catalog` - shows test scenarios and test cases that are included.
- `run` - runs test cases.

To see command parameters, you can use the `-h` option:
```commandline
puthon testsystem.py -h
```
## Creating test cases

To create a test case, you need to create two objects: a test case and a test scenario. Here is an example 
of a test scenario class:
```python
NAME = "Проверка сетевого взаимодействия"
class TestScenario10(TestScenario):
    def __init__(self):
        self.create_instance_test_cases()

    def create_instance_test_cases(self):
        test_cases = list()
        
        # here you can add your test cases
        test_cases.append(TestCase10_1())
        
        super().__init__(test_cases, NAME)
```
Here is an example of a test case:
```python
NAME = "Проверка возможности сетевого подключения к веб приложению"
class TestCase10_1(TestCase):

    def __init__(self):
        super().__init__(NAME)

    def run(self):
        # this command prints log
        self.print_log("отправка ping запроса на адрес '192.168.19.128'")
        if subprocess.call(command) == 0:
            self.print_log("ping запрос прошел успешно")
            self.complete_successfully()
        else:
            self.print_log("ping запрос прошел неуспешно", TestCasLogStatuses.danger)
            self.complete_with_error()
    def after_test(self):
        pass
```
After you create these classes, you need to include the test scenario class
in `create_instance_all_test_scenarios`method of the `Controller` class, like this:
```python
class Controller(object):

    def create_instance_all_test_scenarios(self) -> list:
        test_scenarios = list()
        
        # adding test scenarios
        test_scenarios.append(TestScenario10())

        self.test_scenarios = test_scenarios
```