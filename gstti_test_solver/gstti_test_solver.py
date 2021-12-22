from enum import Enum
from selenium import webdriver
from typing import Dict

import argparse
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

def eprint(*args, **kwargs) -> None:
    print(*args, file=sys.stderr, **kwargs)

def which_test(test_str: str) -> TestType:
    return tests[test_str] if test_str in tests else TestType.ERROR

def create_solution_list(test_name: str) -> list[str]:
    test_name_path = os.path.join(os.path.dirname(__file__), "solutions", test_name) + ".txt"
    return strip_solution(open(test_name_path, 'r').readlines())

def strip_solution(list: list[str]) -> list[str]:
    stripped_list = []
    for element in list:
        stripped_list.append(element.strip())
    return stripped_list

def login(driver, username: str, password: str) -> None:
    username_field = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtEmail")
    username_field.send_keys(username)
    password_field = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtPassword")
    password_field.send_keys(password)
    login_button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_cmdSubmit")
    login_button.click()

def navigate_to_test(driver, test_value) -> None:
    url = "https://gstti.com/ExamStart.aspx?EID="
    match test_value:
        case TestType.RENEWAL_2_HOUR:
            url += "230"
        case TestType.RENEWAL_3_HOUR:
            url += "231"
        case TestType.RENEWAL_5_HOUR:
            url += "233"
        case TestType.RENEWAL_10_HOUR:
            url += "232"
        case TestType.LICENSE_2_HOUR:
            url += "254"
        case TestType.LICENSE_15_HOUR:
            url += "256"
        case TestType.LICENSE_43_HOUR:
            url += "255"
    driver.get(url)

def complete_test(driver, solutions: list[str]) -> None:
    next_test_question(driver)
    for element in solutions:
        select_answer(driver, element)
        next_test_question(driver)

def next_test_question(driver) -> None:
    button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_cmdNext")
    button.click()

def select_answer(driver, answer: str) -> None:
    answer_id = "ctl00_ContentPlaceHolder1_optAnswer"
    match answer:
        case "A":
            answer_id += "A"
        case "B":
            answer_id += "B"
        case "C":
            answer_id += "C"
        case "D":
            answer_id += "D"
        case _:
            raise ValueError("Unrecognized value in solution list.")
    answer_button = driver.find_element_by_id(answer_id)
    answer_button.click()

def solve_test(username: str, password: str, test_name: str, test_value: TestType) -> None:
    solution_list = create_solution_list(test_name)
    driver = webdriver.Firefox()
    driver.get("https://gstti.com")
    login(driver, username, password)
    navigate_to_test(driver, test_value)
    complete_test(driver, solution_list)
    input("Test Complete: Press Enter to close the window...")
    driver.close()

# gstti_test_solver <username> <password> <test_name>
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solve gstti tests in an automated way")
    parser.add_argument("username",
                        help="a username to log-in to")
    parser.add_argument("password",
                        help="a password to log-in with")
    parser.add_argument("test_name",
                        help="the gstti test that will be taken")
    args = parser.parse_args()
    try:
        solve_test(args.username, args.password, args.test_name, which_test(args.test_name))
        sys.exit()
    except FileNotFoundError:
        sys.exit(errno.ENOENT)
    except ValueError:
        sys.exit(errno.EPERM)
