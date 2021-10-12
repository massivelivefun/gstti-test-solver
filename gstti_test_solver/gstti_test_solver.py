from enum import Enum
from selenium import webdriver
from typing import Dict, List

import errno
import os
import sys

class TestType(Enum):
    ### ERROR ENUM VALUE
    ERROR = 0,
    ### LICENSE ENUM VALUES
    # 10 Questions
    LICENSE_2_HOUR = 1
    # 130 Questions
    LICENSE_15_HOUR = 2
    # 270 Questions
    LICENSE_43_HOUR = 3
    ### RENEWAL ENUM VALUES
    # 10 Questions
    RENEWAL_2_HOUR = 4
    # 15 Questions
    RENEWAL_3_HOUR = 5
    # 25 Questions
    RENEWAL_5_HOUR = 6
    # 50 Questions
    RENEWAL_10_HOUR = 7

tests: Dict[str, TestType] = {
    "license2": TestType.LICENSE_2_HOUR,
    "license15": TestType.LICENSE_15_HOUR,
    "license43": TestType.LICENSE_43_HOUR,
    "renewal2": TestType.RENEWAL_2_HOUR,
    "renewal3": TestType.RENEWAL_3_HOUR,
    "renewal5": TestType.RENEWAL_5_HOUR,
    "renewal10": TestType.RENEWAL_10_HOUR
}

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def which_test(test_str: str) -> TestType:
    return tests[test_str] if test_str in tests else TestType.ERROR

def strip_solution(list: list[str]) -> list:
    stripped_list: List = []
    for element in list:
        stripped_list.append(element.strip())
    return stripped_list

def login(driver, username: str, password: str):
    usernamefield = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtEmail")
    usernamefield.send_keys(username)
    passwordfield = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtPassword")
    passwordfield.send_keys(password)
    login_button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_cmdSubmit")
    login_button.click()

def navigate_to_test(driver, test_value):
    match test_value:
        case TestType.RENEWAL_2_HOUR:
            driver.get("https://gstti.com/ExamStart.aspx?EID=230")
        case TestType.RENEWAL_3_HOUR:
            driver.get("https://gstti.com/ExamStart.aspx?EID=231")
        case TestType.RENEWAL_5_HOUR:
            driver.get("https://gstti.com/ExamStart.aspx?EID=233")
        case TestType.RENEWAL_10_HOUR:
            driver.get("https://gstti.com/ExamStart.aspx?EID=232")
        case TestType.LICENSE_2_HOUR:
            driver.get("https://gstti.com/ExamStart.aspx?EID=254")
        case TestType.LICENSE_15_HOUR:
            driver.get("https://gstti.com/ExamStart.aspx?EID=256")
        case TestType.LICENSE_43_HOUR:
            driver.get("https://gstti.com/ExamStart.aspx?EID=255")

def next_test_question(driver):
    button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_cmdNext")
    button.click()

def select_answer(driver, answer: str):
    action = "ctl00_ContentPlaceHolder1_optAnswer"
    match answer:
        case "A":
            action += "A"
        case "B":
            action += "B"
        case "C":
            action += "C"
        case "D":
            action += "D"
        case _:
            raise ValueError('unrecognized value in solutions list')
    button = driver.find_element_by_id(action)
    button.click()

def start_test(driver, solutions: list[str]):
    next_test_question(driver)
    for element in solutions:
        select_answer(driver, element)
        next_test_question(driver)

def solve_test(username: str, password: str, test_name: str, test_value: TestType):
    # Need to fix path handling
    # cur_path = os.path.dirname(__file__)
    # solutions_path = os.path.relpath('./solutions', cur_path)
    test_name_path = "gstti_test_solver/solutions/" + test_name + ".txt"
    # print(cur_path)
    # print(os.getcwd())
    file = open(test_name_path, 'r')
    answers = file.readlines()
    solution_list = strip_solution(answers)
    
    driver = webdriver.Firefox()
    driver.get("https://gstti.com")
    
    login(driver, username, password)
    navigate_to_test(driver, test_value)
    start_test(driver, solution_list)
    
    input("Test Complete: Press Enter to close the window...")
    driver.close()

# gstti_test_solver <username> <password> <test_name>

if __name__ == "__main__":
    if len(sys.argv) == 4:
        test = which_test(sys.argv[3])
        if test == TestType.ERROR:
            eprint("Unrecognized <test_name>: probably not a valid test...")
            eprint("\tgstti_test_solver <username> <password> <test_name>")
            sys.exit(errno.ENOENT)
        solve_test(sys.argv[1], sys.argv[2], sys.argv[3], test)
        sys.exit()
    else:
        eprint("This script is expecting to take only four arguments...")
        eprint("\tgstti_test_solver <username> <password> <file_name>")
        sys.exit(errno.EPERM)
