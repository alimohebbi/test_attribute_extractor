import glob
import pandas as pd
from utils.atm_parser import atm_parse
from utils.craftdroid_parser import craftdroid_parse
from utils.utils import *
import time
import unittest
import json
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
                
def set_element_actions(parsed_event, element_attributes):
    actions = []
    for action in parsed_event["action"]:
        if action["type"] == "replaceText":
            actions.append(str(action["type"])+": "+str(action["value"]))
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

def is_a_match(element, selectors):
    for i in range(1, len(selectors)):
        selector = selectors[i]
        identifier = selector["type"].lower()
        if identifier=="isdisplayed":
            if element.get_attribute("displayed") != 'true':
                return False
        else:
            value = selector["value"]
            if element.get_attribute(identifier).lower() != value.lower():
                return False
    return True

def get_matching_element(parsed_event, elements, log_fname):
    selectors = parsed_event["get_element_by"]
    if len(selectors) == 1:
        if len(elements) >= 1:
            return elements[0]
            if len(elements) > 1:
                error_message = 40*"#"+" ERROR! "+40*"#"+"\nMore than one element was found given the widget selector in line: "+str(parsed_event)+"\n\n\n"
                write_to_error_log(error_message, log_fname)
        else:        
            return None
    for element in elements:
        match = is_a_match(element, selectors)
        if match == True:
            return element
    error_message = 40*"#"+" ERROR! "+40*"#"+"\nNone of the elements fully matches the given widget selectors in line: "+str(parsed_event)+"\n\n\n"
    write_to_error_log(error_message, log_fname)
    return None

def get_elements_by_class_name(driver, class_name, log_fname):
    elements = driver.find_elements_by_class_name(class_name)
    if len(elements)==0:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with class name: "+str(class_name)+", was found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
    return elements

def get_elements_by_xpath(driver, xpath, log_fname):
    elements = driver.find_elements_by_xpath("/hierarchy"+str(xpath))
    if len(elements)==0:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with xpath: "+str(xpath)+", was found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
    return elements

def get_elements_by_text(driver, text, log_fname):
    elements = driver.find_elements_by_android_uiautomator('new UiSelector().text(\"'+str(text)+'\")')
    if len(elements)==0:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with text: "+str(text)+", was found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
    return elements

def get_elements_by_content_desc(driver, content_desc, log_fname):
    elements = driver.find_elements_by_android_uiautomator('new UiSelector().description(\"'+str(content_desc)+'\")')
    if len(elements)==0:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with content description: "+str(content_desc)+", was found on this page source."+"\n\n\n"
        write_to_error_log(error_message, log_fname)
    return elements

def get_elements_by_id(driver, resource_id, app_package, log_fname):
    elements =  driver.find_elements_by_id(app_package+":id/"+str(resource_id))
    if len(elements)==0: 
        elements =  driver.find_elements_by_id("android:id/"+str(resource_id))
        if len(elements)==0:
            error_message = 40*"#"+" ERROR! "+40*"#"+"\nNo element with id: "+str(resource_id)+", was found on this page source."+"\n\n\n"
            write_to_error_log(error_message, log_fname)
    return elements

def get_elements(driver, selector, app_package, log_fname): 
    identifier = selector[0]
    value = selector[1]
    if identifier == "resource-id":
        elements = get_elements_by_id(driver, value, app_package, log_fname)    
    elif identifier == 'contentdescription':
        elements = get_elements_by_content_desc(driver, value, log_fname)
    elif identifier == "text":
        elements = get_elements_by_text(driver, value, log_fname)
    elif identifier == "xpath":
        elements = get_elements_by_xpath(driver, value, log_fname)
    elif identifier == "classname":
        elements = get_elements_by_class_name(driver, value, log_fname)
    else:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nUnknown identifier of the element: "+str(identifier)+", in selector: "+str(selector)+"\n\n\n"
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

def execute_check_element_absence(driver, condition, app_package, log_fname):
    elements = get_elements(driver, (condition["type"], condition["value"]), app_package, log_fname)
    if len(elements) != 0:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nFor check_element_absence, an element with selector: "+str(condition)+"was found!\n\n\n"
        write_to_error_log(error_message, log_fname)

def execute_check_element_presence(driver, condition, app_package, log_fname):
    elements = get_elements(driver, (condition["type"], condition["value"]), app_package, log_fname)
    if len(elements) == 0:
        error_message = 40*"#"+" ERROR! "+40*"#"+"\nFor check_element_presence, The element with selector: "+str(condition)+"was not found!\n\n\n"
        write_to_error_log(error_message, log_fname)

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

def execute_replace_text(action, element, driver):
    element.set_value(action["value"])
    if driver.is_keyboard_shown():
        driver.back()

def execute_action(driver, el, parsed_event, app_package, log_fname):
    executed = True
    for action in parsed_event["action"]:
        if action["type"] == "click":
            el.click()
        elif action["type"] == "longClick":
            TouchAction(driver).long_press(el).release().perform()
        elif action["type"] == "pressBack":
            driver.back()
        elif action["type"] == "replaceText":
            execute_replace_text(action, el, driver)
        elif action["type"] == "enter":
            driver.press_keycode(66)
        elif action["type"] == "wait":
            time.sleep(action["value"])
        elif action["type"].startswith("swipe"):
            execute_swipe(action["type"], el, driver)
        elif action["type"] == "check":
            execute_check(action["value"], el, log_fname)
        elif action["type"] == "check_element_presence":
            execute_check_element_presence(driver, action["value"], app_package, log_fname)
        elif action["type"] == "check_element_absence":
            execute_check_element_absence(driver, action["value"], app_package, log_fname)
        else:
            executed = False
            write_to_error_log("Unhendled event: "+str(action["type"])+", in line: "+str(parsed_event), log_fname)
        time.sleep(5)
    return executed

def get_element_attributes_list(parsed_test, app_package, driver, log_fname):
    element_attributes_list = []
    completed = True
    for parsed_event in parsed_test:
        if len(parsed_event["get_element_by"])==0:
            executed = execute_action(driver, None, parsed_event, app_package, log_fname)
        else:
            el = get_element(driver, parsed_event, app_package, log_fname)
            if el is None:
                completed = False
                break
            element_attributes_list.append(get_element_attributes(el, parsed_event))
            executed = execute_action(driver, el, parsed_event, app_package, log_fname)
            if not executed:
                completed = False
                break
    return element_attributes_list, completed

def run_craftdroid(file, caps, app_package, driver):
    start_time = time.time()
    print(file.split("/")[-1])
    log_fname = file.replace(file.split("/")[-1], "atm_compatible/"+file.split("/")[-1]+"_run_log.txt")
    parsed_test = craftdroid_parse(file)
    element_attributes_list, completed = get_element_attributes_list(parsed_test, app_package, driver, log_fname)
    if completed == True:
        write_json(element_attributes_list, file.replace(file.split("/")[-1], "atm_compatible/"+file.split("/")[-1]+"_result.txt"))
        print(str(time.time() - start_time)+" seconds\n")
    else:
        write_to_error_log("STOPPING THE EXECUTION OF THE TEST!", log_fname)
        print("UNABLE TO RUN THE WHOLE TEST FOR THE FILE :"+str(file)+".PLEASE CHECK THE ERROR LOG!")
        print(str(time.time() - start_time)+" seconds\n")

def run_atm(file, caps, app_package, driver):
    start_time = time.time()
    print('/'.join(file.split("/")[-2:]))
    log_fname = file.replace(file[-5:], "_run_log.txt")
    parsed_test = atm_parse(file)
    element_attributes_list, completed = get_element_attributes_list(parsed_test, app_package, driver, log_fname)
    if completed == True:
        write_json(element_attributes_list, file.replace(file[-5:], '_result.json'))
        print(str(time.time() - start_time)+" seconds\n")
    else:
        write_to_error_log("STOPPING THE EXECUTION OF THE TEST!", log_fname)
        print("UNABLE TO RUN THE WHOLE TEST FOR THE FILE :"+str(file)+".PLEASE CHECK THE ERROR LOG!")
        print(str(time.time() - start_time)+" seconds\n")

def check_run_possible(app_package, caps):
    if app_package is None:
        print("UNABLE TO RUN THE TEST FOR THE FILE :"+file+".")
        return False, None
    try:
        driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)
    except:
        print("UNABLE TO GRAB THE DRIVER WITH CAPABILITIES :"+str(caps)+".")
        return False, None
    return True, driver

def main():
    files = glob.glob('data/*/*/*.java')
    files.extend(glob.glob("data/craftdroid_tests/*/b*2/base/*.json"))
    for file in files:
        print(file)
        caps, app_package = get_caps(file)
        run_possible, driver = check_run_possible(app_package, caps)
        if run_possible:
            if file.split("/")[-3] == "migrated_tests" or file.split("/")[-3] == "donor":
                run_atm(file, caps, app_package, driver)
            else:
                if file.split("/")[-6] == "craftdroid_tests":
                    run_craftdroid(file, caps, app_package, driver)           

if __name__ == '__main__':
    main()
