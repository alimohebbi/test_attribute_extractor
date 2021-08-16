import os, sys
import toml
import glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import test_attribute_extractor

with open('config.toml', 'r') as file:
        config = toml.load(file)

def main():
    migration_configs = glob.glob(config['data']['MIGRATION_CONFIGS']['address'])
    for migration_config in migration_configs:
    	files = glob.glob(migration_config+"/*/*.java")
    	for file in files:
            final_fname = "/".join(file.split("/")[0:-1])
            log_fname = "/".join([final_fname, file.split("/")[-1].split(".")[0]+ '_log.txt'])
            final_fname = "/".join([final_fname, file.split("/")[-1].split(".")[0]+".json"])
            try:
                test_attribute_extractor.ATMExtractor(file, log_fname).write_results(final_fname)
            except Exception as e:
                print(f"Running {file} failed with error {e}")
    	
    
if __name__ == '__main__':
    main()