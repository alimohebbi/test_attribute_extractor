import logging
import pathlib
import sys
import os
from abc import ABC, abstractmethod

sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute()))

import glob
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from utils.utils import *
from utils.atm_parser import atm_parse
from utils.craftdroid_parser import craftdroid_parse
from utils.configuration import Configuration

config = Configuration()


class TestAttributeExtractor(ABC):
    def __init__(self, file_name: str, log_address = ""):
        self.name = file_name
        self.logger = self.get_logger(log_address)
        caps, self.app_package = get_caps(self.name)
        self.driver = self.check_run_possible(self.app_package, caps)
        self.attribute_list = ["checkable", "checked", "class", "clickable", "content-desc", "enabled", "focusable",
                               "focused", "long-clickable", "package", "password", "resource-id", "scrollable",
                               "selection-start",
                               "selection-end", "selected", "text", "bounds", "displayed"]

    def get_logger(self, log_address):
        if log_address == "":
            name = self._get_log_file_name()
            logger = logging.getLogger(name)
            log_path = os.path.join(config.logs_dir, name)
            log_directory = "/".join(log_path.split("/")[0:-1])
            isExist = os.path.exists(log_directory)
            if not isExist:
                os.makedirs(log_directory)
            fh = logging.FileHandler(log_path, mode='w')
        else:
            logger = logging.getLogger(log_address)
            fh = logging.FileHandler(log_address, mode='w')
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

    def check_run_possible(self, app_package, caps):
        if app_package is None:
            self.logger.error(f"UNABLE TO RUN THE TEST FOR THE FILE: {self.name}.")
            raise ValueError("app package is None")
        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)
            return driver
        except Exception as e:
            self.logger.error(f"UNABLE TO GRAB THE DRIVER WITH CAPABILITIES: {str(caps)}.")
            self.logger.exception(e)
            raise

    @abstractmethod
    def _get_log_file_name(self):
        pass

    @abstractmethod
    def _get_result_file_name(self):
        pass

    def get_condition(self, parsed_event, index):
        conditional = parsed_event["action"][index]
        if conditional == "id":
            conditional = "resource-id"
        value = parsed_event["action"][index + 1]
        return conditional, value
    
    def execute_check_element_invisible(self, parsed_event):
        oracle_pass = True
        condition = [parsed_event["action"][2], parsed_event["action"][3]]
        elements = self.get_elements((condition[0], condition[1]))
        if len(elements) != 0:
            error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nFor check_element_invisible, an element with selector: " + str(
                condition) + ", was found!\n\n\n"
            self.logger.error(error_message)
            oracle_pass = False
        return oracle_pass

    def execute_check_element_presence(self, element, parsed_event):
        oracle_pass = True
        i = 2
        while i < len(parsed_event["action"]):
            conditional, value = self.get_condition(parsed_event, i)
            if conditional == "isDisplayed":
                if element.get_attribute("displayed") != value:
                    oracle_pass = False
            elif conditional == "isEnabled":
                if element.get_attribute("enabled") != value:
                    oracle_pass = False
            elif conditional == "text":
                if preprocess_text(value) not in preprocess_text(element.get_attribute("text")):
                    oracle_pass = False
            elif conditional == 'contentdescription' or conditional == "content-desc":
                if preprocess_text(value) not in preprocess_text(element.get_attribute("content-desc")):
                    oracle_pass = False
            elif conditional == "id" or conditional == "resource-id":
                if value != element.get_attribute(conditional):
                    if value != element.get_attribute(conditional).split("/")[1]:
                        oracle_pass = False
            elif conditional in self.attribute_list:
                if value != element.get_attribute(conditional):
                    oracle_pass = False
            else:
                error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nUnknown attribute for check: " + str(
                    (conditional, value)) + "\n\n\n"
                self.logger.error(error_message)
                oracle_pass = False
            i += 2
        if not oracle_pass:
            error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nConditions not fully satisfied in: " + str(
                parsed_event) + "\n\n\n"
            self.logger.error(error_message)
        return oracle_pass

    def execute_swipe(self, action, element):
        direction = action.split("_")[1]
        size = element.size
        if direction == "left":
            start_x = int(size['width'] * 0.9)
            start_y = int(size['height'] / 2)
            end_x = int(size["width"] * 0.05)
            end_y = start_y
        elif direction == "right":
            start_x = int(size["width"] * 0.05)
            start_y = int(size['height'] / 2)
            end_x = int(size['width'] * 0.9)
            end_y = start_y
        elif direction == "up":
            start_x = int(size['width'] / 2)
            start_y = int(size["height"] * 0.7)
            end_x = start_x
            end_y = int(size["height"] * 0.3)
        elif direction == "down":
            start_x = int(size['width'] / 2)
            start_y = int(size["height"] * 0.3)
            end_x = start_x
            end_y = int(size["height"] * 0.7)
        TouchAction(self.driver).press(element, start_x, start_y).wait(ms=300).move_to(element, end_x, end_y).release().perform()

    def execute_send_keys(self, action, value, element):
        if "enter" in action:
            element.click()
            element.set_value(value)
            self.driver.press_keycode(66)
        else:
            element.set_value(value)
        if self.driver.is_keyboard_shown():
            self.driver.back()

    def execute_action(self, el, parsed_event):
        oracle_pass = True
        executed = True
        action = parsed_event["action"][0]
        if action == "click":
            el.click()
        elif action == "long_press":
            TouchAction(self.driver).long_press(el).release().perform()
        elif action == "KEY_BACK":
            self.driver.back()
        elif "clear" in action:
            el.clear()
            if "send_keys" in action:
                self.execute_send_keys(action, parsed_event["action"][1], el)
        elif "send_keys" in action:
            self.execute_send_keys(action, parsed_event["action"][1], el)
        elif action.startswith("swipe"):
            self.execute_swipe(action, el)
        elif "wait" in action:
            if action == "wait_until_element_presence" or action == "wait_until_text_presence":
                oracle_pass = self.execute_check_element_presence(el, parsed_event)
            elif action == "wait_until_text_invisible":
                oracle_pass = self.execute_check_element_invisible(parsed_event)
        else:
            executed = False
            self.logger.error("Unhendled event: " + str(action) + ", in line: " + str(parsed_event))
        time.sleep(5)
        return executed, oracle_pass

    def is_a_match(self, element, selectors):
        for i in range(1, len(selectors)):
            selector = selectors[i]
            identifier = selector["type"]
            value = selector["value"]
            if value is not None:
                value = value.lower()
            element_value = element.get_attribute(identifier)
            if element_value is not None:
                element_value = element_value.lower()
            if identifier == "isdisplayed":
                if element.get_attribute("displayed") != 'true':
                    return False
            elif identifier == "text":
                test_value = 'date' if is_date(value) else value
                element_value = 'date' if is_date(element_value) else element_value
                if test_value not in element_value:
                    return False
            elif element_value != value:
                return False
        return True

    def get_matching_element(self, parsed_event, elements):
        selectors = parsed_event["get_element_by"]
        if len(selectors) == 1:
            if len(elements) >= 1:
                return elements[0]
            else:
                if parsed_event["action"][0].startswith("wait"):
                    error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nNo element with selector: " + str(
                    selectors[0]) + ", was found on this page source." + "\nConditions not fully satisfied in: " + str(
                parsed_event) + "\n\n\n"
                else:
                    error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nNo element with selector: " + str(
                    selectors[0]) + ", was found on this page source." + "\n\n\n"
                self.logger.error(error_message)
                return None
        for element in elements:
            match = self.is_a_match(element, selectors)
            if match:
                return element
        if parsed_event["action"][0]!= "wait_until_text_invisible" or parsed_event["action"][0]!= "KEY_BACK":
            error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nNone of the elements fully matches the given widget selectors in line: " + str(
                parsed_event) + "\n\n\n"
            self.logger.error(error_message)
        return None

    def get_elements_by_xpath(self, xpath):
        elements = self.driver.find_elements_by_xpath("/hierarchy" + str(xpath))
        if len(elements) == 0:
            elements = self.driver.find_elements_by_xpath(str(xpath))
        return elements

    def get_elements_by_id(self, resource_id):
        elements = self.driver.find_elements_by_id(self.app_package + ":id/" + str(resource_id))
        if len(elements) == 0:
            elements = self.driver.find_elements_by_id("android:id/" + str(resource_id))
            if len(elements) == 0:
                elements = self.driver.find_elements_by_id(str(resource_id))
        return elements

    def get_elements_by_text(self, text):
        elements = []
        original_elements = self.driver.find_elements_by_android_uiautomator(
                'new UiSelector().text(\"' + str(text) + '\")')
        elements = Union(elements, original_elements)
        if len(elements) == 0:
            case_permutations = list(all_casings(text))
            for permutation in case_permutations:
                new_elements = self.driver.find_elements_by_android_uiautomator(
                'new UiSelector().text(\"' + str(permutation) + '\")')
                elements = Union(elements, new_elements)
        return elements

    def get_elements(self, selector):
        identifier = selector[0]
        value = selector[1]
        if identifier == "resource-id" or identifier == "id":
            elements = self.get_elements_by_id(value)
        elif identifier == 'contentdescription':
            elements = self.driver.find_elements_by_android_uiautomator(
                'new UiSelector().descriptionContains(\"' + str(value) + '\")')
        elif identifier == "text":
            elements = self.get_elements_by_text(value)
        elif identifier == "xpath":
            elements = self.get_elements_by_xpath(value)
        elif identifier == "classname":
            elements = self.driver.find_elements_by_class_name(value)
        else:
            error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nUnknown identifier of the element: " + str(
                identifier) + ", in selector: " + str(selector) + "\n\n\n"
            self.logger.error(error_message)
            return None
        return elements

    def skip_internal_activity(self):
        i = 0
        while(i< 5):
            if self.driver.current_activity == "android/com.android.internal.app.ResolverActivity":
                self.driver.back()
                time.sleep(5)
                i += 1
            else:
                break

    def get_element(self, parsed_event, skipped_internal_activity = False):
        identifier = parsed_event["get_element_by"][0]["type"]
        value = parsed_event["get_element_by"][0]["value"]
        elements = self.get_elements((identifier, value))
        if elements is None or not len(elements):
            if not skipped_internal_activity:
                self.skip_internal_activity()
                elements = self.get_elements((identifier, value))
        element = self.get_matching_element(parsed_event, elements)
        return element

    def set_event_type(self, action):
        if action == "KEY_BACK":
            return ("SYS_EVENT")
        elif "wait" in action:
            return "oracle"
        else:
            return "gui"

    def get_element_attributes(self, element, parsed_event):
        element_attributes = {}
        for attr in self.attribute_list:
            element_attributes[attr] = element.get_attribute(attr)
        element_attributes["action"] = parsed_event["action"]
        element_attributes["event_type"] = self.set_event_type(parsed_event["action"][0])
        element_attributes['page'] = get_page_source(self.driver)
        element_attributes['activity'] = self.driver.current_activity
        return element_attributes

    def get_text_invisibl_element_attributes(self, parsed_event, oracle_pass):
        element_attributes = {}
        element_attributes['oracle_pass'] = oracle_pass
        element_attributes["action"] = parsed_event["action"]
        element_attributes["event_type"] = self.set_event_type(parsed_event["action"][0])
        element_attributes['page'] = get_page_source(self.driver)
        element_attributes['activity'] = self.driver.current_activity
        for i, item in parsed_event["action"]:
            if item in ['class', 'resource-id', 'text', 'content-desc', 'clickable', 'password']:
                element_attributes[attr] = element.get_attribute(attr)
        return element_attributes

    def handle_wait(self, parsed_event, element_attributes_list):
        oracle_pass = False
        if parsed_event["action"][0] == "wait_until_text_invisible":
            executed, oracle_pass = self.execute_action(None, parsed_event)
            element_attributes = self.get_text_invisibl_element_attributes(parsed_event, oracle_pass)
            element_attributes_list.append(element_attributes)
        else:
            el = self.get_element(parsed_event)
            if el is None:
                element_attributes = self.get_text_invisibl_element_attributes(parsed_event, oracle_pass)
                element_attributes_list.append(element_attributes)
            else:
                executed, oracle_pass = self.execute_action(el, parsed_event)
                element_attributes = self.get_element_attributes(el, parsed_event)
                element_attributes['oracle_pass'] = oracle_pass
                element_attributes_list.append(element_attributes)
        return element_attributes_list

    def get_element_attributes_list(self, parsed_test):
        time.sleep(10)
        element_attributes_list = []
        completed = True
        for parsed_event in parsed_test:
            while self.driver.is_keyboard_shown():
               self.driver.back()
               time.sleep(5)
            if "wait" in parsed_event["action"][0]:
                time.sleep(parsed_event["action"][1])
                element_attributes_list = self.handle_wait(parsed_event, element_attributes_list)
            else:
                if parsed_event["action"][0] == "KEY_BACK":
                    executed, execute_action = self.execute_action(None, parsed_event)
                    element_attributes_list.append(parsed_event)
                else:
                    el = self.get_element(parsed_event)
                    if el is None:
                        completed = False
                        break
                    element_attributes_list.append(self.get_element_attributes(el, parsed_event))
                    executed, execute_action = self.execute_action(el, parsed_event)
                if not executed:
                    completed = False
                    break
        return element_attributes_list, completed

    @abstractmethod
    def get_parsed_test(self):
        pass

    def run(self):
        start_time = time.time()
        parsed_test = self.get_parsed_test()
        element_attributes_list, completed = self.get_element_attributes_list(parsed_test)
        print(str(time.time() - start_time) + " seconds\n")
        if completed:
            return element_attributes_list
        else:
            self.logger.error("STOPPING THE EXECUTION OF THE TEST!")
            self.logger.error(
                "UNABLE TO RUN THE WHOLE TEST FOR THE FILE :" + str(self.name) + ".PLEASE CHECK THE ERROR LOG!")
            return None

    def write_results(self, address):
        element_attributes_list = self.run()
        if address == "":
            write_json(element_attributes_list, os.path.join(config.results_dir, self._get_result_file_name()))
        else:
            write_json(element_attributes_list, address)
            

class CraftdroidExtractor(TestAttributeExtractor):

    def _get_log_file_name(self):
        return "craftdroid_tests/"+self.name.split("/")[-3]+"_"+self.name.split("/")[-1].split(".")[0] + '_log.txt'

    def _get_result_file_name(self):
        return "craftdroid_tests/"+self.name.split("/")[-3]+"_"+self.name.split("/")[-1].split(".")[0] + '_attributes.json'

    def get_parsed_test(self):
        parsed_test = craftdroid_parse(self.name)
        return parsed_test


class ATMExtractor(TestAttributeExtractor):

    def _get_log_file_name(self):
        relative_address = self.name.split("/")[-4]+"/"+self.name.split("/")[-3]+"/"
        subject_name = self.name.split("/")[-2]+"/"+self.name.split("/")[-1].split(".")[0]
        return relative_address + subject_name + '_log.txt'

    def _get_result_file_name(self):
        relative_address = self.name.split("/")[-4]+"/"+self.name.split("/")[-3]+"/"
        subject_name = self.name.split("/")[-2]+"/"+self.name.split("/")[-1].split(".")[0]
        return relative_address + subject_name + '_attributes.json'

    def get_parsed_test(self):
        parsed_test = atm_parse(self.name)
        return parsed_test


def main():
    atm_globs = config.custom_tests_glob('atm')
    # craftdroid_globs = config.custom_tests_glob('craftdroid')

    for file in atm_globs:
        print(file)
        try:
            ATMExtractor(file).write_results("")
        except Exception as e:
            print(f"Running {file} failed with error {e}")

    # for file in craftdroid_globs:
    #     print(file)
    #     try:
    #         CraftdroidExtractor(file).write_results("")
    #     except Exception as e:
    #         print(f"Running {file} failed with error {e}")


if __name__ == '__main__':
    main()
