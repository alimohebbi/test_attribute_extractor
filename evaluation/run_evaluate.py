import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evaluation.ground_truth_to_generated_mapper import extract_all_ground_truth_generated_maps
from evaluation.evaluate import evaluate_all_configs
from evaluation.aggregate_final_results import sift_erroneous_migrations, aggregate_results


def main():
    extract_all_ground_truth_generated_maps()
    evaluate_all_configs()
    sift_erroneous_migrations()
    aggregate_results()


if __name__ == '__main__':
    main()
