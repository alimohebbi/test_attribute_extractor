import glob
import pandas as pd
from utils.parser import parse
import time
import unittest
import json
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException

def write_jsons(attribute_list, file):
    with open(file.replace('.java', '.json'), 'w') as f:
        f.write(json.dumps(attribute_list, indent=2))

def execute_replace_text(action, element, driver):
    element.set_value(action["value"])
    if driver.is_keyboard_shown():
        driver.back()

def execute_action(driver, el, dictionary):
    executed = True
    for action in dictionary["action"]:
        if action["type"] == "replaceText":
            execute_replace_text(action, el, driver)
        elif action["type"] == "click":
            el.click()
        elif action["type"] == "check":
            continue
        elif action["type"] == "longClick":
            TouchAction(driver).long_press(el).perform()
 #       elif action["type"] == "swipeLeft":
#driver.execute_script("mobile: scroll", {"direction": "left", element: el, "toVisible": True})
        elif action["type"] == "check":
            pass
        else:
            executed = False
            print("Unknown event: "+str(action["type"]))
    return executed
                
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

def get_element_by_id(driver, dictionary, app_package):
    try:
        element =  driver.find_element_by_id(app_package+":id/"+dictionary["get_element_by"]["value"])
        return element
    except NoSuchElementException:
        try:
            element =  driver.find_element_by_id("android:id/"+dictionary["get_element_by"]["value"])
            return element
        except NoSuchElementException:
            print("No element with id:"+dictionary["get_element_by"]["value"]+" found on this page source.")
            return None

def get_element_by_content_desc(driver, dictionary, app_package):
    try:
        element = driver.find_element_by_android_uiautomator('new UiSelector().description(\"'+dictionary["get_element_by"]["value"]+'\")')
        return element
    except:
        print("No element with content description:"+dictionary["get_element_by"]["value"]+" found on this page source.")
        return None

def get_element_by_text(driver, dictionary, app_package):
    try:
        element = driver.find_element_by_android_uiautomator('new UiSelector().text(\"'+dictionary["get_element_by"]["value"]+'\")')
        return element
    except:
        print("No element with text:"+dictionary["get_element_by"]["value"]+" found on this page source.")
        return None

def get_element_by_xpath(driver, dictionary, app_package):
    try:
        element = driver.find_element_by_xpath("/hierarchy"+dictionary["get_element_by"]["value"])
        return element
    except:
        print("No element with xpath:"+dictionary["get_element_by"]["value"]+" found on this page source.")
        return None

def get_element_by_class_name(driver, dictionary, app_package):
    try:
        element = driver.find_element_by_class_name(dictionary["get_element_by"]["value"])
        return element
    except:
        print("No element with id:"+dictionary["get_element_by"]["value"]+" found on this page source.")
        return None

def get_element(driver, dictionary, app_package):
    identifier = dictionary["get_element_by"]["type"]
    if identifier == "Id":
        element = get_element_by_id(driver, dictionary, app_package)    
    elif identifier == 'ContentDescription':
        element = get_element_by_content_desc(driver, dictionary, app_package)
    elif identifier == "Text":
        element = get_element_by_text(driver, dictionary, app_package)
    elif identifier == "XPath":
        element = get_element_by_xpath(driver, dictionary, app_package)
    elif identifier == "ClassName":
        element = get_element_by_class_name(driver, dictionary, app_package)
    else:
        print("Unknown identifier of the element in line: " + str(dictionary))
        return None
    return element

def get_attribute_list(parsed_test, app_package, driver):
    attribute_list = []
    completed = True
    for line in parsed_test:
        if len(line) !=1:
            el = get_element(driver, line, app_package)
            if el is None:
                completed = False
                break
            attribute_list.append(get_element_attributes(el, line))
            executed = execute_action(driver, el, line)
            if not executed:
                completed = False
                break
        else:
            driver.back()
        time.sleep(5)
    return attribute_list, completed

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
    app_package, app_activity = get_package_activity(file, df)
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
        start_time = time.time()
        print(file.split("/")[-2:])
        parsed_test, caps, app_package = read_file(file)
        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)
        except:
            continue
        attribute_list, completed = get_attribute_list(parsed_test, app_package, driver)
        if completed == False:
            print("ERROR!\n"+40*"#")
            print("Unable to run the whole test for the :"+str(file))
        write_jsons(attribute_list, file)
        print(str(time.time() - start_time)+" seconds\n")

if __name__ == '__main__':
    main()
