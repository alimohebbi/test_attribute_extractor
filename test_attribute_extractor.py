import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.absolute()))

import glob
import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from utils.utils import *
from utils.atm_parser import atm_parse
from utils.craftdroid_parser import craftdroid_parse, config

attribute_list = ["checkable", "checked", "class", "clickable", "content-desc", "enabled", "focusable",
                  "focused", "long-clickable", "package", "password", "resource-id", "scrollable", "selection-start",
                  "selection-end", "selected", "text", "bounds", "displayed"]

def set_event_type(action):
    if action == "KEY_BACK":
        return("SYS_EVENT")
    elif "wait" in action:
        return "oracle"
    else:
        return "gui"

def get_element_attributes(element, parsed_event):
    element_attributes = {}
    for attr in attribute_list:
        element_attributes[attr] = element.get_attribute(attr)
    element_attributes["action"] = parsed_event["action"]
    element_attributes["event_type"]= set_event_type(parsed_event["action"][0])
    return element_attributes


def is_a_match(element, selectors):
    for i in range(1, len(selectors)):
        selector = selectors[i]
        identifier = selector["type"]
        value = selector["value"]
        if identifier == "isdisplayed":
            if element.get_attribute("displayed") != 'true':
                return False
        elif identifier == "text":
            if value.lower() not in element.get_attribute(identifier).lower():
                return False

        elif element.get_attribute(identifier).lower() != value.lower():
            return False
    return True


def get_matching_element(parsed_event, elements, log_fname):
    selectors = parsed_event["get_element_by"]
    if len(selectors) == 1:
        if len(elements) >= 1:
            return elements[0]
        if len(elements) > 1:
            error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nMore than one element was found given the widget selector in line: " + str(
                parsed_event) + "\n\n\n"
            write_to_error_log(error_message, log_fname)
        else:
            error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nNo element with selector: " + str(
                selectors[0]) + ", was found on this page source." + "\n\n\n"
            write_to_error_log(error_message, log_fname)
            return None
    for element in elements:
        match = is_a_match(element, selectors)
        if match:
            return element
    if actions_need_element(parsed_event["action"]):
        error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nNone of the elements fully matches the given widget selectors in line: " + str(
            parsed_event) + "\n\n\n"
        write_to_error_log(error_message, log_fname)
    return None


def get_elements_by_xpath(driver, xpath, log_fname):
    elements = driver.find_elements_by_xpath("/hierarchy" + str(xpath))
    if len(elements) == 0:
        elements = driver.find_elements_by_xpath(str(xpath))
    return elements


def get_elements_by_id(driver, resource_id, app_package, log_fname):
    elements = driver.find_elements_by_id(app_package + ":id/" + str(resource_id))
    if len(elements) == 0:
        elements = driver.find_elements_by_id("android:id/" + str(resource_id))
        if len(elements) == 0:
            elements = driver.find_elements_by_id(str(resource_id))
    return elements


def get_elements(driver, selector, app_package, log_fname):
    identifier = selector[0]
    value = selector[1]
    if identifier == "resource-id" or identifier == "id":
        elements = get_elements_by_id(driver, value, app_package, log_fname)
    elif identifier == 'contentdescription':
        elements = driver.find_elements_by_android_uiautomator(
            'new UiSelector().descriptionContains(\"' + str(value) + '\")')
    elif identifier == "text":
        elements = driver.find_elements_by_android_uiautomator('new UiSelector().textContains(\"' + str(value) + '\")')
    elif identifier == "xpath":
        elements = get_elements_by_xpath(driver, value, log_fname)
    elif identifier == "classname":
        elements = driver.find_elements_by_class_name(value)
    else:
        error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nUnknown identifier of the element: " + str(
            identifier) + ", in selector: " + str(selector) + "\n\n\n"
        write_to_error_log(error_message, log_fname)
        return None
    return elements


def get_element(driver, parsed_event, app_package, log_fname):
    identifier = parsed_event["get_element_by"][0]["type"]
    value = parsed_event["get_element_by"][0]["value"]
    elements = get_elements(driver, (identifier, value), app_package, log_fname)
    if elements is None:
        return None
    element = get_matching_element(parsed_event, elements, log_fname)
    return element


def execute_check_element_invisible(driver, parsed_event, app_package, log_fname):
    condition = [parsed_event["action"][2], parsed_event["action"][3]]
    elements = get_elements(driver, (condition[0], condition[1]), app_package, log_fname)
    if len(elements) != 0:
        error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nFor check_element_invisible, an element with selector: " + str(
            condition) + ", was found!\n\n\n"
        write_to_error_log(error_message, log_fname)


def get_condition(parsed_event, index):
    conditional = parsed_event["action"][index]
    if conditional == "id":
        conditional = "resource-id"
    value = parsed_event["action"][index + 1]
    return conditional, value


def execute_check_element_presence(element, parsed_event, app_package, log_fname):
    matched = True
    i = 2
    while i < len(parsed_event["action"]):
        conditional, value = get_condition(parsed_event, i)
        if conditional == "isDisplayed":
            if element.get_attribute("displayed") != value:
                matched = False
        elif conditional == "isEnabled":
            if element.get_attribute("enabled") != value:
                matched = False
        elif conditional == "text":
            if preprocess_text(value) not in preprocess_text(element.get_attribute("text")):
                matched = False
        elif conditional == "id" or conditional == "resource-id":
            if value != element.get_attribute(conditional):
                if value != element.get_attribute(conditional).split("/")[1]:
                    matched = False
        elif conditional in attribute_list:
            if value != element.get_attribute(conditional):
                matched = False
        else:
            error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nUnknown attribute for check: " + str(
                (conditional, value)) + "\n\n\n"
            write_to_error_log(error_message, log_fname)
            matched = False
        i += 2
    if not matched:
        error_message = 40 * "#" + " ERROR! " + 40 * "#" + "\nConditions not fully satisfied in: " + str(
            parsed_event) + "\n\n\n"
        write_to_error_log(error_message, log_fname)


def execute_swipe(action, element, driver):
    direction = action.split("_")[1]
    location = element.location
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
    TouchAction(driver).press(element, start_x, start_y).wait(ms=300).move_to(element, end_x, end_y).release().perform()


def execute_send_keys(action, value, element, driver):
    element.set_value(value)
    if driver.is_keyboard_shown():
        driver.back()
    if "enter" in action:
        driver.press_keycode(66)


def execute_action(driver, el, parsed_event, app_package, log_fname):
    executed = True
    action = parsed_event["action"][0]
    if action == "click":
        el.click()
    elif action == "long_press":
        TouchAction(driver).long_press(el).release().perform()
    elif action == "KEY_BACK":
        driver.back()
    elif "clear" in action:
        el.clear()
        if "send_keys" in action:
            execute_send_keys(action, parsed_event["action"][1], el, driver)
    elif "send_keys" in action:
        execute_send_keys(action, parsed_event["action"][1], el, driver)
    elif action.startswith("swipe"):
        execute_swipe(action, el, driver)
    elif "wait" in action:
        if action == "wait_until_element_presence" or action == "wait_until_text_presence":
            execute_check_element_presence(el, parsed_event, app_package, log_fname)
        elif action == "wait_until_text_invisible":
            execute_check_element_invisible(driver, parsed_event, app_package, log_fname)
    else:
        executed = False
        write_to_error_log("Unhendled event: " + str(action) + ", in line: " + str(parsed_event), log_fname)
    time.sleep(5)
    return executed


def get_element_attributes_list(parsed_test, app_package, driver, log_fname):
    time.sleep(10)
    element_attributes_list = []
    completed = True
    for parsed_event in parsed_test:
        if "wait" in parsed_event["action"][0]:
            time.sleep(parsed_event["action"][1])
        if not actions_need_element(parsed_event["action"]):
            executed = execute_action(driver, None, parsed_event, app_package, log_fname)
        else:
            el = get_element(driver, parsed_event, app_package, log_fname)
            if el is None:
                completed = False
                break
            element_attr = get_element_attributes(el, parsed_event)
            element_attr['page'] = get_page_source(driver)
            element_attr['activity'] = driver.current_activity
            element_attributes_list.append(element_attr)
            executed = execute_action(driver, el, parsed_event, app_package, log_fname)
            if not executed:
                completed = False
                break
    return element_attributes_list, completed


def run_craftdroid(file):
    caps, app_package = get_caps(file)
    run_possible, driver = check_run_possible(app_package, caps)
    if run_possible:
        start_time = time.time()
        log_fname = file.replace(file.split("/")[-1], "result/" + file.split("/")[-1].split(".")[0] + "_run_log.txt")
        parsed_test = craftdroid_parse(file)
        element_attributes_list, completed = get_element_attributes_list(parsed_test, app_package, driver, log_fname)
        if completed:
            write_json(element_attributes_list, file.replace(file.split("/")[-1],
                                                             "result/" + file.split("/")[-1].split(".")[
                                                                 0] + "_result.json"))
            print(str(time.time() - start_time) + " seconds\n")
        else:
            write_to_error_log("STOPPING THE EXECUTION OF THE TEST!", log_fname)
            print("UNABLE TO RUN THE WHOLE TEST FOR THE FILE :" + str(file) + ".PLEASE CHECK THE ERROR LOG!")
            print(str(time.time() - start_time) + " seconds\n")


def run_atm(file):
    caps, app_package = get_caps(file)
    run_possible, driver = check_run_possible(app_package, caps)
    if run_possible:
        start_time = time.time()
        log_fname = file.replace(file[-5:], "_run_log.txt")
        parsed_test = atm_parse(file)
        element_attributes_list, completed = get_element_attributes_list(parsed_test, app_package, driver, log_fname)
        if completed == True:
            write_json(element_attributes_list, file.replace(file[-5:], '_result.json'))
            print(str(time.time() - start_time) + " seconds\n")
        else:
            write_to_error_log("STOPPING THE EXECUTION OF THE TEST!", log_fname)
            print("UNABLE TO RUN THE WHOLE TEST FOR THE FILE :" + str(file) + ".PLEASE CHECK THE ERROR LOG!")
            print(str(time.time() - start_time) + " seconds\n")


def check_run_possible(app_package, caps):
    if app_package is None:
        print("UNABLE TO RUN THE TEST FOR THE FILE :" + file + ".")
        return False, None
    try:
        driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)
    except:
        print("UNABLE TO GRAB THE DRIVER WITH CAPABILITIES :" + str(caps) + ".")
        return False, None
    return True, driver


def main():
    atm_globs = config.custom_tests_glob('atm')
    craftdroid_globs = config.custom_tests_glob('craftdroid')

    for file in atm_globs:
        run_atm(file)

    for file in craftdroid_globs:
        run_craftdroid(file)

if __name__ == '__main__':
    main()
