import glob
import pandas as pd
from utils.parser import parse
from utils.utils import *
import time
import unittest
import json
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException

def execute_replace_text(action, element, driver):
    element.set_value(action["value"])
    if driver.is_keyboard_shown():
        driver.back()

def execute_action(driver, el, parsed_event, log_fname):
    executed = True
    for action in parsed_event["action"]:
        if action["type"] == "replaceText":
            execute_replace_text(action, el, driver)
        elif action["type"] == "click":
            el.click()
        elif action["type"] == "check":
            continue
        elif action["type"] == "longClick":
            TouchAction(driver).long_press(el).release().perform()
        #       elif action["type"] == "swipeLeft":
        #driver.execute_script("mobile: scroll", {"direction": "left", element: el, "toVisible": True})
        else:
            executed = False
            write_to_error_log("Unhendled event: "+str(action["type"])+", in line: "+str(parsed_event), log_fname)
    return executed
                
def set_element_actions(parsed_event, element_attributes):
    actions = []
    for action in parsed_event["action"]:
        if action["type"] == "replaceText":
            actions.append(action["type"]+":"+action["value"])
        else:
            actions.append(action["type"])

    element_attributes["action"] = actions
    return element_attributes

def set_element_appium_attributes(parsed_event, element_attributes):   
    attribute_list =  ["checkable", "checked", "class", "clickable", "content-desc", "enabled", "focusable",
    "focused","long-clickable", "package", "password", "resource-id", "scrollable","selection-start",
    "selection-end", "selected", "text", "bounds", "displayed"]
    
    for attr in attribute_list:
        element_attributes[attr] = element.get_attribute(attr)

    return element_attributes

def get_element_attributes(element, parsed_event):
    element_attributes = {}

    element_attributes = set_element_appium_attributes(parsed_event, element_attributes)
    element_attributes = set_element_actions(parsed_event, element_attributes)
    
    return element_attributes

def get_element_by_id(driver, resource_id, app_package, log_fname):
    try:
        element =  driver.find_element_by_id(app_package+":id/"+str(resource_id))
        return element
    except NoSuchElementException:
        try:
            element =  driver.find_element_by_id("android:id/"+str(resource_id))
            return element
        except NoSuchElementException:
            error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with id: "+str(resource_id)+", was found on this page source."+"\n\n\n"
            write_to_error_log(error_message, log_fname)
            return None

def get_element_by_content_desc(driver, content_desc, log_fname):
    try:
        element = driver.find_element_by_android_uiautomator('new UiSelector().description(\"'+str(content_desc)+'\")')
        return element
    except:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with content description: "+str(content_desc)+", was found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
        return None

def get_element_by_text(driver, text, log_fname):
    try:
        element = driver.find_element_by_android_uiautomator('new UiSelector().text(\"'str(text)+'\")')
        return element
    except:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with text: "+str(text)+", was found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
        return None

def get_element_by_xpath(driver, xpath, log_fname):
    try:
        element = driver.find_element_by_xpath("/hierarchy"str(xpath))
        return element
    except:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with xpath: "+str(xpath)+", was found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
        return None

def get_element_by_class_name(driver, class_name, log_fname):
    try:
        element = driver.find_element_by_class_name(class_name)
        return element
    except:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with class name: "+str(class_name)+", was found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
        return None

def get_element(driver, parsed_event, app_package, log_fname):
    identifier = parsed_event["get_element_by"]["type"]
    value = parsed_event["get_element_by"]["value"]
    if identifier == "Id":
        element = get_element_by_id(driver, value, app_package, log_fname)    
    elif identifier == 'ContentDescription':
        element = get_element_by_content_desc(driver, value, log_fname)
    elif identifier == "Text":
        element = get_element_by_text(driver, value, log_fname)
    elif identifier == "XPath":
        element = get_element_by_xpath(driver, value, log_fname)
    elif identifier == "ClassName":
        element = get_element_by_class_name(driver, value, log_fname)
    else:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nUnknown identifier of the element: "+str(identifier)+", in line: "+str(parsed_event)+"\n\n\n"
        write_to_error_log(error_message, log_fname)
        return None
    return element

def get_element_attributes_list(parsed_test, app_package, driver, log_fname):
    element_attributes_list = []
    completed = True
    for parsed_event in parsed_test:
        if len(parsed_event) == 1:
            driver.back()
        else:
            el = get_element(driver, parsed_event, app_package, log_fname)
            if el is None:
                completed = False
                break
            element_attributes_list.append(get_element_attributes(el, parsed_event))
            executed = execute_action(driver, el, parsed_event, log_fname)
            if not executed:
                completed = False
                break
        time.sleep(5)
    return element_attributes_list, completed

def check_run_possible(app_package, caps):
    if app_package is None:
        print("UNABLE TO RUN THE TEST FOR THE FILE :"+str(file)+".")
        return False, None
    try:
        driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)
    except:
        print("UNABLE TO GRAB THE DRIVER WITH CAPABILITIES :"+str(caps)+".")
        return False, None
    return True, driver

def main():
    files = glob.glob('data/*/*/*.java')
    for file in files:
        print(file.split("/")[-2:])
        log_fname = file.replace('.json', "_log.txt")
        start_time = time.time()
        caps, app_package = get_caps(file)
        run_possible, driver = check_run_possible(app_package, caps)
        if run_possible:
            parsed_test = parse(file)
            element_attributes_list, completed = get_element_attributes_list(parsed_test, app_package, driver, log_fname)
            if completed == False:
                write_to_error_log("STOPPING THE EXECUTION OF THE TEST!", log_fname)
                print("UNABLE TO RUN THE WHOLE TEST FOR THE FILE :"+str(file)+"."++"PLEASE CHECK THE ERROR LOG!")
            write_json(element_attributes_list, file, '.json')
            print(str(time.time() - start_time)+" seconds\n")

if __name__ == '__main__':
    main()
