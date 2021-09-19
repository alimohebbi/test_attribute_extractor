import toml
import glob
import os
import json
import pandas as pd
import shutil

with open('config.toml', 'r') as file:
        config = toml.load(file)

def load_json_data(fname):
    f = open(fname, )
    data = json.load(f)
    return data

def sift_erroneous_migrations():
	erroneous_generated = config['data']['MIGRATION_CONFIGS']['erroneous_address']
	migration_configs = glob.glob(config['data']['MIGRATION_CONFIGS']['address'])
	for migration_config in migration_configs:
		migrations = glob.glob(migration_config+"/*")
		for migration in migrations:
			log_fname = glob.glob(migration + "/*_log.txt")[0]
			with open(log_fname) as f:
				lines = f.readlines()
			if len(lines):
				erroneous_address = erroneous_generated+"/"+'/'.join(migration.split("/")[-2:])
				if not os.path.exists(erroneous_address):
					shutil.copytree(migration, erroneous_address)
	
def aggregate_results():
	config_list = []
	number_of_migrations_list = []
	number_of_errors_list = []
	number_of_blocking_errors_list = []
	erroneous_generated = config['data']['MIGRATION_CONFIGS']['erroneous_address']
	migration_configs = glob.glob(config['data']['MIGRATION_CONFIGS']['address'])

	for migration_config in migration_configs:

		config_list.append(migration_config.split("/")[-1])

		number_of_migrations_list.append(len(glob.glob(migration_config+"/*")))

		erroneous_migrations = glob.glob(erroneous_generated+"/"+migration_config.split("/")[-1]+"/*")
		number_of_errors_list.append(len(erroneous_migrations))

		num_blocking_errors = 0
		for migration in erroneous_migrations:
			if load_json_data(glob.glob(migration+"/*_final.json")[0]) is None:
				num_blocking_errors += 1
		number_of_blocking_errors_list.append(num_blocking_errors)

	aggregated_result = pd.DataFrame({'config': config_list, 'migrations': number_of_migrations_list,
		'errors': number_of_errors_list, 'blocking_errors':number_of_blocking_errors_list})
	aggregated_result.to_csv(config['data']['result']['aggregated_result_address'], index = False)

def main():
	sift_erroneous_migrations()
	aggregate_results()

if __name__ == '__main__':
    main()