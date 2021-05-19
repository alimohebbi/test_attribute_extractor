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

def execute_replace_text(action, element, driver):
    element.set_value(action["value"])
    if driver.is_keyboard_shown():
        driver.back()

def execute_check(conditions, element, log_fname):
    matched = True
    for condition in conditions:    
        condition["type"] = condition["type"].replace(" ", "")
        if condition["type"] =="isDisplayed":
            if element.get_attribute("displayed") != 'true':
                matched = False
        elif condition["type"] =="isEnabled":
            if element.get_attribute("enabled") != 'true':
                matched = False
        elif condition["type"] == "text":
            if condition["value"].lower() != element.get_attribute("text").lower():
                matched = False
        else:
            error_message = 40*"#"+" ERROR! "+40*"#"+"\nUnknown attribute for check: "+str(condition)+"\n\n\n"
            write_to_error_log(error_message, log_fname)
    if matched == False:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nConditions not fully satisfied in: "+str(conditions)+"\n\n\n"
        write_to_error_log(error_message, log_fname)
    return matched

def execute_swipe(action, element, driver):
    direction = action.split("swipe")[1].lower()
    location = element.location
    size = element.size
    if direction == "left":
        start_x = location['x']+50
        start_y = location['y']+int(size['height']/2)
        end_x = int(location['x']-size['width']*(2.0/3))
        end_y = start_y
    elif direction == "right":
        start_x = location['x']+50
        start_y = location['y']+int(size['height']/2)
        end_x = int(location['x']+size['width']*(2.0/3))
        end_y = start_y
    elif direction == "up":
        start_x = location['x']+int(size['width']/2)
        start_y = location['y']+50
        end_x = start_x
        end_y = int(location['y']-size['height']*(2.0/3))
    elif direction == "down":
        start_x = location['x']+int(size['width']/2)
        start_y = location['y']+50
        end_x = start_x
        end_y = int(location['y']+size['height']*(2.0/3))
    TouchAction(driver).press(element, start_x, start_y).move_to(element, end_x, end_y).release().perform()
        
def execute_action(driver, el, parsed_event, log_fname):
    executed = True
    for action in parsed_event["action"]:
        if action["type"] == "replaceText":
            execute_replace_text(action, el, driver)
        elif action["type"] == "click":
            el.click()
        elif action["type"] == "check":
            execute_check(action["value"], el, log_fname)
        elif action["type"] == "longClick":
            TouchAction(driver).long_press(el).release().perform()
        elif action["type"].startswith("swipe"):
            execute_swipe(action["type"], el, driver)
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

def set_element_appium_attributes(element, element_attributes):   
    attribute_list =  ["checkable", "checked", "class", "clickable", "content-desc", "enabled", "focusable",
    "focused","long-clickable", "package", "password", "resource-id", "scrollable","selection-start",
    "selection-end", "selected", "text", "bounds", "displayed"]
    
    for attr in attribute_list:
        element_attributes[attr] = element.get_attribute(attr)

    return element_attributes

def get_element_attributes(element, parsed_event):
    element_attributes = {}

    element_attributes = set_element_appium_attributes(element, element_attributes)
    element_attributes = set_element_actions(parsed_event, element_attributes)
    
    return element_attributes

def get_elements_by_id(driver, resource_id, app_package, log_fname):
    elements =  driver.find_elements_by_id(app_package+":id/"+str(resource_id))
    if len(elements)==0: 
        elements =  driver.find_elements_by_id("android:id/"+str(resource_id))
        if len(elements)==0:
            error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with id: "+str(resource_id)+", was found on this page source."+"\n\n\n"
            write_to_error_log(error_message, log_fname)
    return elements

def get_elements_by_content_desc(driver, content_desc, log_fname):
    elements = driver.find_elements_by_android_uiautomator('new UiSelector().description(\"'+str(content_desc)+'\")')
    if len(elements)==0:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with content description: "+str(content_desc)+", was found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
    return elements

def get_elements_by_text(driver, text, log_fname):
    elements = driver.find_elements_by_android_uiautomator('new UiSelector().text(\"'+str(text)+'\")')
    if len(elements)==0:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with text: "+str(text)+", was found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
    return elements

def get_elements_by_xpath(driver, xpath, log_fname):
    elements = driver.find_elements_by_xpath("/hierarchy"+str(xpath))
    if len(elements)==0:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with xpath: "+str(xpath)+", was found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
    return elements

def get_elements_by_class_name(driver, class_name, log_fname):
    elements = driver.find_elements_by_class_name(class_name)
    if len(elements)==0:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with class name: "+str(class_name)+", was found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
    return elements

def is_a_match(element, selectors):
    match = True
    for i in range(1, len(selectors)):
        selector = selectors[i]
        identifier = selector["type"].lower()
        if identifier=="isdisplayed":
            if element.get_attribute("displayed") != 'true':
                match = False
        else:
            value = selector["value"]
            if element.get_attribute(identifier).lower() != value.lower():
                match = False
    return match

def get_matching_element(parsed_event, elements, log_fname):
    selectors = parsed_event["get_element_by"]
    if len(selectors) == 1:
        if len(elements) == 1:
            return elements[0]
        else:
            if len(elements) > 1:
                error_message = 40*"#"+" ERROR! "+40*"#"+"\nMore than one element was found given the widget selector in line: "+str(parsed_event)+"\n\n\n"
                write_to_error_log(error_message, log_fname)
                return elements[0]
            return None
    for element in elements:
        match = is_a_match(element, selectors)
        if match == True:
            return element
    error_message = 40*"#"+" ERROR! "+40*"#"+"\nNone of the elements fully matches the given widget selectors in line: "+str(parsed_event)+"\n\n\n"
    write_to_error_log(error_message, log_fname)
    return None

def get_element(driver, parsed_event, app_package, log_fname):
    identifier = parsed_event["get_element_by"][0]["type"]
    value = parsed_event["get_element_by"][0]["value"]
    if identifier == "resource-id":
        elements = get_elements_by_id(driver, value, app_package, log_fname)    
    elif identifier == 'ContentDescription':
        elements = get_elements_by_content_desc(driver, value, log_fname)
    elif identifier == "Text":
        elements = get_elements_by_text(driver, value, log_fname)
    elif identifier == "XPath":
        elements = get_elements_by_xpath(driver, value, log_fname)
    elif identifier == "ClassName":
        elements = get_elements_by_class_name(driver, value, log_fname)
    else:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nUnknown identifier of the element: "+str(identifier)+", in line: "+str(parsed_event)+"\n\n\n"
        write_to_error_log(error_message, log_fname)
        return None
    element = get_matching_element(parsed_event, elements, log_fname)
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
        log_fname = file.replace('.java', "_log.txt")
        start_time = time.time()
        caps, app_package = get_caps(file)
        run_possible, driver = check_run_possible(app_package, caps)
        if run_possible:
            parsed_test = parse(file)
            element_attributes_list, completed = get_element_attributes_list(parsed_test, app_package, driver, log_fname)
            if completed == True:
                write_json(element_attributes_list, file, '.json')
                print(str(time.time() - start_time)+" seconds\n")
            else:
                write_to_error_log("STOPPING THE EXECUTION OF THE TEST!", log_fname)
                print("UNABLE TO RUN THE WHOLE TEST FOR THE FILE :"+str(file)+".PLEASE CHECK THE ERROR LOG!")
                print(str(time.time() - start_time)+" seconds\n")
            

if __name__ == '__main__':
    main()
