import argparse
import json
import os, sys
import toml
import glob
from Levenshtein import distance
import emulator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import test_attribute_extractor
from evaluation.emulator import start_emulator, stop_emulator

with open('config.toml', 'r') as file:
        config = toml.load(file)
ALGORITHM = str(config["algorithm"])

def prune_files(files):
    dummy_file_indices = set()
    for i in range(len(files)):
        for j in range(len(files)):
            if distance(files[i], files[j]) == 1 and files[i][-6]!= files[j][-6]:
                if files[i] < files[j]: 
                    dummy_file_indices.add(i)
    return [i for j, i in enumerate(files) if j not in dummy_file_indices]

def load_json_data(fname):
    f = open(fname, )
    data = json.load(f)
    return data

def already_exists(final_fname):
    if os.path.isfile(final_fname):
        if load_json_data(final_fname) is not None:
            return True
    return False

def get_file_addressed(file):
    migration = file.split("/")[-2]

    base_final_address = config[ALGORITHM]['BASE_JSON_ADDRESS']['address']+"/".join(file.split("/")[3:5])
    if not os.path.exists(base_final_address):
        os.mkdir(base_final_address)
    if not os.path.exists(base_final_address + "/"+migration):
        os.mkdir(base_final_address + "/"+migration)
    final_fname = base_final_address + "/"+migration+"/"+file.split("/")[-1].split(".")[0]+"_final.json"

    base_log_address = config[ALGORITHM]['BASE_LOG_ADDRESS']['address']+"/".join(file.split("/")[3:5])
    if not os.path.exists(base_log_address):
        os.mkdir(base_log_address)
    if not os.path.exists(base_log_address + "/"+migration):
        os.mkdir(base_log_address + "/"+migration)
    log_fname = base_log_address + "/"+migration+"/"+file.split("/")[-1].split(".")[0]+"_log.txt"

    return final_fname, log_fname

def run(file, log_fname, final_fname):
    start_emulator()
    if ALGORITHM == "atm":
        try:
            test_attribute_extractor.ATMExtractor(file, log_fname).write_results(final_fname)
        except Exception as e:
            print(f"Running {file} failed with error {e}")
    elif ALGORITHM == "craftdroid":
        try:
            test_attribute_extractor.CraftdroidExtractor(file, log_fname).write_results(final_fname)
        except Exception as e:
            print(f"Running {file} failed with error {e}")
    else:
            print("Unknown algorithm: "+str(algorithm))
    stop_emulator()

def main():
    migration_configs = glob.glob(config[ALGORITHM]['MIGRATION_CONFIGS']['address'])
    for migration_config in migration_configs:
        print(migration_config+'\n')
        files = glob.glob(migration_config+"/*/*.java")
        if ALGORITHM == "atm":
            files = prune_files(files)
        for file in files:
            final_fname, log_fname = get_file_addressed(file)
            print(final_fname+'\n')
            if already_exists(final_fname):
                continue
            run(file, log_fname, final_fname)
            with open(log_fname) as f:
                lines = f.readlines()
            if len(lines) and lines[0].startswith("UNABLE TO GRAB THE DRIVER WITH CAPABILITIES"):
                print('\n'+"RUNNING AGAIN: "+'\n')
                run(file, log_fname, final_fname)               
    
if __name__ == '__main__':
    main()