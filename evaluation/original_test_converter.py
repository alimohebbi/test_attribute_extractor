import glob
import json
import os
import sys

import toml
from Levenshtein import distance

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import test_attribute_extractor
from evaluation.emulator import start_emulator, stop_emulator

with open('../config_template/config.toml', 'r') as file:
    config = toml.load(file)
ALGORITHM = str(config["algorithm"])
NUM_RUNS = 1


def prune_files(files):
    dummy_file_indices = set()
    for i in range(len(files)):
        for j in range(len(files)):
            if distance(files[i], files[j]) == 1 and files[i][-6] != files[j][-6]:
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


def get_file_addresses(file):
    migration = file.split("/")[-2]
    sm_config_id = file.split("/")[-3]
    test_file_name = file.split("/")[-1].split(".")[0]
    base_final_address = config[ALGORITHM]['BASE_JSON_ADDRESS']['generated'] + sm_config_id
    if not os.path.exists(base_final_address):
        os.mkdir(base_final_address)
    if not os.path.exists(base_final_address + "/" + migration):
        os.mkdir(base_final_address + "/" + migration)
    final_fname = base_final_address + "/" + migration + "/" + test_file_name + "_final.json"

    base_log_address = config[ALGORITHM]['BASE_LOG_ADDRESS']['generated'] + sm_config_id
    if not os.path.exists(base_log_address):
        os.mkdir(base_log_address)
    if not os.path.exists(base_log_address + "/" + migration):
        os.mkdir(base_log_address + "/" + migration)
    log_fname = base_log_address + "/" + migration + "/" + test_file_name + "_log.txt"

    return final_fname, log_fname


def run(file):
    final_fname, log_fname = get_file_addresses(file)
    if already_exists(final_fname):
        return
    print(final_fname + '\n')
    start_emulator()
    if ALGORITHM == "atm":
        try:
            extractor = test_attribute_extractor.ATMExtractor(file, log_fname)
            extractor.write_results(final_fname)
        except Exception as e:
            print(f"Running {file} failed with error {e}")
    elif ALGORITHM == "craftdroid":
        try:
            test_attribute_extractor.CraftdroidExtractor(file, log_fname).write_results(final_fname)
        except Exception as e:
            print(f"Running {file} failed with error {e}")
    else:
        print("Unknown algorithm: " + str(algorithm))
    stop_emulator()


def run_all_left_migrations():
    migration_configs = glob.glob(config[ALGORITHM]['MIGRATION_CONFIGS']['address'])
    for i in range(NUM_RUNS):
        for migration_config in migration_configs:
            print(migration_config + '\n')
            if ALGORITHM == "atm":
                files = prune_files(glob.glob(migration_config + "/*/*.java"))
            else:
                files = glob.glob(migration_config + "/*/*.json")
            migrations = glob.glob(migration_config + "/*")
            for migration in migrations:
                config_migration = "/".join(migration.split("/")[-2:])
                try:
                    if not len(glob.glob(config[ALGORITHM]['BASE_JSON_ADDRESS']['generated'] + config_migration + "/*_final.json")):
                        for file in files:
                            if config_migration in file:
                                run(file)
                except Exception as e:
                    pass


def main():
    run_all_left_migrations()


if __name__ == '__main__':
    main()
