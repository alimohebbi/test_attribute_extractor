import argparse
import os, sys
import toml
import glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import test_attribute_extractor

with open('config.toml', 'r') as file:
        config = toml.load(file)

def get_args():
    parser = argparse.ArgumentParser(description='Evaluator')
    parser.add_argument('--algorithm', dest='algorithm', type=str, help='migrator algorithm')
    args = parser.parse_args()
    if args.algorithm is None:
        args.algorithm = "atm"
    return args

def get_file_addressed(file):
    final_fname = "/".join(file.split("/")[0:-1])
    log_fname = "/".join([final_fname, file.split("/")[-1].split(".")[0]+ '_log.txt'])
    final_fname = "/".join([final_fname, file.split("/")[-1].split(".")[0]+"_final.json"])
    return final_fname, log_fname

def main():

    args = get_args()
    migration_configs = glob.glob(config['data']['MIGRATION_CONFIGS']['address'])
    for migration_config in migration_configs:
        print()
        print(migration_config)
        print()
        files = glob.glob(migration_config+"/*/*.java")
        for file in files:
            print(file)
            final_fname, log_fname = get_file_addressed(file)
            if args.algorithm == "atm":
                try:
                    test_attribute_extractor.ATMExtractor(file, log_fname).write_results(final_fname)
                except Exception as e:
                    print(f"Running {file} failed with error {e}")
            elif args.algorithm == "craftdroid":
                try:
                    test_attribute_extractor.CraftdroidExtractor(file, log_fname).write_results(final_fname)
                except Exception as e:
                    print(f"Running {file} failed with error {e}")
            else:
                print("Unknown algorithm: "+str(args.algorithm))    
    
if __name__ == '__main__':
    main()