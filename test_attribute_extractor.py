import glob
import pandas as pd
from utils.parser import Parse
import time
import unittest
import json
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction

def execute_action(driver, element, dictionary):
    for action in dictionary["action"]:
        if action["type"] == "replaceText":
            element.set_value(action["value"])
        else:
            if action["type"] == "click":
                element.click()
            elif action["type"] == "longClick":
                TouchAction(driver).long_press(element).perform()
            elif action["type"] == "check":
                continue
                
def get_element_actions(dictionary):
    actions = []
    for action in dictionary["action"]:
        if action["type"] == "replaceText":
            actions.append(action["type"]+":"+action["value"])
        else:
            actions.append(action["type"])
    return actions

def get_element_attributes(element, dictionary):

    element_attributes = {}
    
    attribute_list =  ["checkable", "checked", "class", "clickable", "content-desc", "enabled", "focusable",
    "focused","long-clickable", "package", "password", "resource-id", "scrollable","selection-start",
    "selection-end", "selected", "text", "bounds", "displayed"]
    
    for attr in attribute_list:
        element_attributes[attr] = element.get_attribute(attr)
    
    actions = get_element_actions(dictionary)
        
    element_attributes["action"] = actions
    
    return element_attributes

def get_element(driver, dictionary, app_package):
    identifier = dictionary["get_element_by"]["type"]
    if identifier == "Id":
        element =  driver.find_element_by_id(app_package+":id/"+dictionary["get_element_by"]["value"])
    elif identifier == 'ContentDescription':
        element = driver.find_element_by_android_uiautomator('new UiSelector().description(\"'+dictionary["get_element_by"]["value"]+'\")')
    elif identifier == "Text":
        element = driver.find_element_by_android_uiautomator('new UiSelector().text(\"'+dictionary["get_element_by"]["value"]+'\")')
    elif identifier == "XPath":
        element = driver.find_element_by_xpath("/hierarchy"+dictionary["get_element_by"]["value"])
    elif identifier == "ClassName":
        element = driver.find_element_by_class_name(dictionary["get_element_by"]["value"])
    else:
        print("Unknown identifier of the element in line: " + str(dictionary))
        return
    return element

def get_app_name(fname):
    category = fname.split("/")[-3]
    if category == "migrated_tests":
        return fname.split("/")[-2].split("-")[1]
    elif category == "ground_truth":
        return fname.split("/")[-2]
    else:
        print("The java file should be under directory /data/migrated_tests or /data/ground_truth")
        return

def get_package_activity(fname, df):
    app_name = get_app_name(fname)
    app_package = list(df[df["appName"] == app_name]["appPackage"])[0]
    app_activity = list(df[df["appName"] == app_name]["appActivity"])[0]

    return app_package, app_activity

def read_file(file):
    df = pd.read_csv("app_name_to_package_activity.csv")
    parsed_test = parse(file)
    app_package, app_activity = get_package_activity(fname, df)
    caps = {
        'platformName': 'Android',
        'platformVersion': '7.0',
        'deviceName': 'emulator-5555',
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
