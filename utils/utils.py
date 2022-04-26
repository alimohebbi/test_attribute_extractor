import datetime
import json
import pathlib

import dateinfer
import pandas as pd
import re
from dateutil.parser import parse


def read_file(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
    return lines


def write_to_error_log(message, filename):
    f = open(filename, 'a')
    f.write(message)
    print(message)


def write_json(data, new_name):
    with open(new_name, 'w') as f:
        f.write(json.dumps(data, indent=2))


def load_json_data(fname):
    f = open(fname, )
    data = json.load(f)
    return data


def get_capabilities(app_package, app_activity, no_reset):
    caps = {
        'platformName': 'Android',
        'platformVersion': '6.0',
        'deviceName': 'emulator1',
        'appPackage': app_package,
        'appActivity': app_activity,
        'autoGrantPermissions': True,
        'noReset': no_reset,
        "newCommandTimeout": 50000
    }
    return caps


def get_app_name(fname):
    # category = fname.split("/")[-5]
    # if 'original' in category:
    #     return fname.split("/")[-2].split("-")[1]
    category = fname.split("/")[-3]
    if category == "migrated_tests":
        return fname.split("/")[-2].split("-")[1]
    elif category == "donor":
        return fname.split("/")[-2]
    elif category == "ground_truth":
        if "-" in fname:
            return fname.split("/")[-1].split("-")[1].split(".")[0]
        else:
            return fname.split("/")[-1].split(".")[0]
    elif fname.split("/")[-4] == "generated":
        return fname.split("/")[-2].split("-")[1]
    else:
        category = fname.split("/")[-5]
        if category == "craftdroid_tests" or category == "test_repo":
            return fname.split("/")[-1].split(".")[0]
        else:
            return None


def get_package_activity(fname):
    app_name = get_app_name(fname)
    if app_name is None:
        return None, None
    activity_file_path = str(pathlib.Path(__file__).parent.absolute()) + "/../app_name_to_package_activity.csv"
    df = pd.read_csv(activity_file_path)
    sliced_df = df[df["appName"] == app_name]
    if len(sliced_df) == 0:
        print("No application with the name : " + str(app_name) + " can be found in app_name_to_package_activity.csv.")
        return None, None
    app_package = sliced_df.iloc[0]["appPackage"]
    app_activity = sliced_df.iloc[0]["appActivity"]
    no_reset = sliced_df.iloc[0]["noReset"]

    return app_package, app_activity, no_reset


def get_caps(fname):
    app_package, app_activity, no_reset = get_package_activity(fname)
    if no_reset == 0:
        caps = get_capabilities(app_package, app_activity, False)
    else:
        caps = get_capabilities(app_package, app_activity, True)
    return caps, app_package


def preprocess_text(s):
    return " ".join(re.sub(r'[^\w\s]', '', s.lower()).split())


def get_page_source(driver):
    driver.hide_keyboard()
    page = driver.page_source
    page = page.replace('\r', '')
    page = page.replace('\n', '')
    page = re.sub(r'>[\ ]+<', '><', page)
    return page


def is_date(input_date):
    try:
        parse(input_date, fuzzy=False)
        return True
    except ValueError:
        return False


def actions_need_element(action):
    if action == "KEY_BACK" or action == "wait_until_text_invisible":
        return False
    else:
        return True
        
def update_date(input_date):
    if not is_date(input_date):
        return input_date
    try:
        inferred_format = dateinfer.infer([input_date])
    except Exception as e:
        inferred_format = dateinfer.infer([input_date.replace('-', '/')])
        inferred_format = inferred_format.replace('/', '-')
    inferred_format = inferred_format.replace('%H', '%d')
    today = datetime.date.today()
    modified_date = today.strftime(inferred_format)
    return str(modified_date)

def all_casings(input_string):
    if not input_string:
        yield ""
    else:
        first = input_string[:1]
        if first.lower() == first.upper():
            for sub_casing in all_casings(input_string[1:]):
                yield first + sub_casing
        else:
            for sub_casing in all_casings(input_string[1:]):
                yield first.lower() + sub_casing
                yield first.upper() + sub_casing

def Union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list


if __name__ == '__main__':
    print(update_date('yesterday'))
