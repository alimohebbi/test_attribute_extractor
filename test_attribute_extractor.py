import glob
import pandas as pd
from utils.parser import Parse
import time
import unittest
import json
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction

def get_element(driver, dictionary, app_package):
    identifier = dictionary["get_element_by"][0]
    if identifier == "Id":
        element =  driver.find_element_by_id(app_package+":id/"+dictionary["get_element_by"][1])
    elif identifier == 'ContentDescription':
        element = driver.find_element_by_android_uiautomator('new UiSelector().description(\"'+dictionary["get_element_by"][1]+'\")')
    elif identifier == "Text":
        element = driver.find_element_by_android_uiautomator('new UiSelector().text(\"'+dictionary["get_element_by"][1]+'\")')
    elif identifier == "XPath":
        element = driver.find_element_by_xpath("/hierarchy"+dictionary["get_element_by"][1])
    else:
        print("Unknown identifier of the element in line: " + str(dictionary))
        return
    return element

def execute_action(driver, element, dictionary):
    for action in dictionary["action"]:
        if type(action) is dict and list(action.keys())[0] == "replaceText()":
            element.set_value(list(action.values())[0])
        else:
            if action == "click()":
                element.click()
            elif action == "longClick()":
                TouchAction(driver).long_press(element).perform()
            elif action == "check()":
                continue
            elif action == "closeSoftKeyboard()":
                driver.hide_keyboard()

def get_element_attributes(element, dictionary):

    element_attributes = {}
    
    attribute_list =  ["checkable", "checked", "class", "clickable", "content-desc", "enabled", "focusable",
    "focused","long-clickable", "package", "password", "resource-id", "scrollable","selection-start",
    "selection-end", "selected", "text", "bounds", "displayed"]
    
    for attr in attribute_list:
        element_attributes[attr] = element.get_attribute(attr)
    
    element_attributes["action"] = dictionary["action"]
    
    return element_attributes

def get_app_name(fname):
    category = fname.split("/")[1]
    if category == "migrated_tests":
        return fname.split("/")[2].split("-")[1]
    elif category == "ground_truth":
        return fname.split("/")[2]
    else:
        print("The java file should be under directory /data/migrated_tests or /data/ground_truth")
        return

def get_package_activity(fname):
    app_name = get_app_name(fname)
    app_package = list(df[df["appName"] == app_name]["appPackage"])[0]
    app_activity = list(df[df["appName"] == app_name]["appActivity"])[0]

    return app_package, app_activity

def read_file(file):
    df = pd.read_csv("app_name_to_package_activity.csv")
    parsed_test = parse(file)
    app_package, app_activity = get_package_activity(fname)
    caps = {
        'platformName': 'Android',
        'platformVersion': '7.1.1',
        'deviceName': 'emulator-5554',
        'appPackage': app_package,
        'appActivity': app_activity,
        'autoGrantPermissions': True,
        'noReset': False,
        "newCommandTimeout": 3000
    }
    return parsed_test, caps, app_package

def main():
    files = glob.glob('data/*/*/*.java')
    
    for file in files:
        parsed_test, caps, app_package = read_file(file)
        driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)
        attribute_list = []
        for line in parsed_test:
            if len(line) !=1:
                el = get_element(driver, line, app_package)
                attribute_list.append(get_element_attributes(el, line))
                execute_action(driver, el, line)
                time.sleep(5)
            else:
                driver.back()
        with open(file.replace('.java', '.json'), 'w') as f:
                f.write(json.dumps(attribute_list, indent=2))

if __name__ == '__main__':
    main()
