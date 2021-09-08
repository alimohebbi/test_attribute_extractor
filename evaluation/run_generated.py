import argparse
import os, sys
import toml
import glob
from Levenshtein import distance
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

def prune_files(files):
    dummy_file_indices = set()
    for i in range(len(files)):
        for j in range(len(files)):
            if distance(files[i], files[j]) == 1 and files[i][-6]!= files[j][-6]:
                if files[i] < files[j]: 
                    dummy_file_indices.add(i)
    return [i for j, i in enumerate(files) if j not in dummy_file_indices]

def get_file_addressed(file):
    final_fname = "/".join(file.split("/")[0:-1])
    log_fname = "/".join([final_fname, file.split("/")[-1].split(".")[0]+ '_log.txt'])
    final_fname = "/".join([final_fname, file.split("/")[-1].split(".")[0]+"_final.json"])
    return final_fname, log_fname

def run(algorithm, file, log_fname, final_fname):
    if algorithm == "atm":
        try:
            test_attribute_extractor.ATMExtractor(file, log_fname).write_results(final_fname)
        except Exception as e:
            print(f"Running {file} failed with error {e}")
    elif algorithm == "craftdroid":
        try:
            test_attribute_extractor.CraftdroidExtractor(file, log_fname).write_results(final_fname)
        except Exception as e:
            print(f"Running {file} failed with error {e}")
    else:
            print("Unknown algorithm: "+str(algorithm))

def main():
    args = get_args()
    migration_configs = glob.glob(config['data']['MIGRATION_CONFIGS']['address'])
    for migration_config in migration_configs:
        print(migration_config+'\n')
        files = glob.glob(migration_config+"/*/*.java")
        if args.algorithm == "atm":
            files = prune_files(files)
        for file in files:
            final_fname, log_fname = get_file_addressed(file)
            print(final_fname+'\n')
            if os.path.isfile(final_fname):
                continue
            run(args.algorithm, file, log_fname, final_fname)
            with open(log_fname) as f:
                lines = f.readlines()
            if len(lines) and lines[0].startswith("UNABLE TO GRAB THE DRIVER WITH CAPABILITIES"):
                print('\n'+"RUNNING AGAIN: "+'\n')
                run(args.algorithm, file, log_fname, final_fname)


                
    
if __name__ == '__main__':
    main()