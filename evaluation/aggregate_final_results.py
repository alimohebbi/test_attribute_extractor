import toml
import glob
import os
import json
import pandas as pd
import shutil

with open('../config_template/config.toml', 'r') as file:
    config = toml.load(file)
ALGORITHM = str(config["algorithm"])


def load_json_data(fname):
    f = open(fname, )
    data = json.load(f)
    return data


def sift_erroneous_migrations():
    erroneous_generated = config[ALGORITHM]['MIGRATION_CONFIGS']['erroneous_address']
    migration_configs = glob.glob(config[ALGORITHM]['MIGRATION_CONFIGS']['address'])
    for migration_config in migration_configs:
        # print(migration_config)
        migrations = glob.glob(migration_config + "/*")
        for migration in migrations:
            # print(migration)
            config_migration = "/".join(migration.split("/")[-2:])
            try:
                log_fname = glob.glob(config[ALGORITHM]['BASE_LOG_ADDRESS']['generated'] + config_migration + "/*_log.txt")[0]
                with open(log_fname) as f:
                    lines = f.readlines()
                if len(lines):
                    erroneous_address = erroneous_generated + '/'.join(migration.split("/")[-2:])
                    if not os.path.exists(erroneous_address):
                        shutil.copytree(migration, erroneous_address)
                    shutil.copyfile(log_fname, erroneous_address+"/"+log_fname.split("/")[-1])
                    try:
                        final_fname = glob.glob(config[ALGORITHM]['BASE_JSON_ADDRESS']['generated'] + config_migration + "/*_final.json")[0]
                        shutil.copyfile(final_fname, erroneous_address+"/"+final_fname.split("/")[-1])
                    except Exception as e:
                        pass
            except Exception as e:
                pass
        for migration in migrations:
            config_migration = "/".join(migration.split("/")[-2:])
            try:
                erroneous_address = erroneous_generated + '/'.join(migration.split("/")[-2:])
                if not len(glob.glob(config[ALGORITHM]['BASE_JSON_ADDRESS']['generated'] + config_migration + "/*_final.json")):
                    log_fname = glob.glob(config[ALGORITHM]['BASE_LOG_ADDRESS']['generated'] + config_migration + "/*_log.txt")[0]
                    if not os.path.exists(erroneous_address):
                        shutil.copytree(migration, erroneous_address)
                        shutil.copyfile(log_fname, erroneous_address+"/"+log_fname.split("/")[-1])
            except Exception as e:
                pass


def aggregate_results():
    config_list = []
    number_of_migrations_list = []
    number_of_problematic_errors_list = []
    number_of_blocking_errors_list = []
    number_of_driver_errors_list = []
    number_of_oracle_errors_list = []
    erroneous_generated = config[ALGORITHM]['MIGRATION_CONFIGS']['erroneous_address']
    migration_configs = glob.glob(config[ALGORITHM]['BASE_JSON_ADDRESS']['generated']+"/*")
    for migration_config in migration_configs:
        config_list.append(migration_config.split("/")[-1])

        number_of_migrations_list.append(len(glob.glob(migration_config + "/*")))

        erroneous_migrations = glob.glob(erroneous_generated+ migration_config.split("/")[-1] + "/*")
        num_blocking_errors = 0
        num_driver_errors = 0
        num_oracle_errors = 0
        for migration in erroneous_migrations:
            if not len(glob.glob(migration + "/*_final.json")):
                num_driver_errors += 1
            elif load_json_data(glob.glob(migration + "/*_final.json")[0]) is None:
                num_blocking_errors += 1
            else:
                num_oracle_errors += 1
        number_of_blocking_errors_list.append(num_blocking_errors)
        number_of_driver_errors_list.append(num_driver_errors)
        number_of_oracle_errors_list.append(num_oracle_errors)
        number_of_problematic_errors_list.append(num_blocking_errors + num_driver_errors)

    aggregated_result = pd.DataFrame({'config': config_list, 'migrations': number_of_migrations_list,
                                      'problematic_errors': number_of_problematic_errors_list,
                                      'blocking_errors': number_of_blocking_errors_list,
                                      'driver_errors' : number_of_driver_errors_list,
                                      'oracle_errors' : number_of_oracle_errors_list})
    aggregated_result.to_csv(config[ALGORITHM]['result']['aggregated_result_address'], index=False)


def main():
    sift_erroneous_migrations()
    aggregate_results()


if __name__ == '__main__':
    main()
