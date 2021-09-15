import os
import glob
import yaml


class Configuration(object):

    def __init__(self):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(THIS_FOLDER, '../config.yml')
        with open(path, 'r') as ymlfile:
            self._config = yaml.load(ymlfile, Loader=yaml.FullLoader)

    @property
    def parsed_test_dir(self):
        return self._get_property('parsed_test_dir')

    @property
    def logs_dir(self):
        return self._get_property('logs_dir')

    @property
    def results_dir(self):
        return self._get_property('results_dir')

    @property
    def analyse_dir(self):
        return self._get_property('analyse_dir')

    def custom_tests_glob(self, name):
        tests = self._get_property('tests')
        if tests is None or name not in tests:
            return None
        custom_tests = tests[name]
        globes = glob.glob("")
        for glob_str in custom_tests['file_globs']:
            globes.extend(glob.glob(f"{custom_tests['dir']}/{glob_str}"))
        return globes

    def _get_property(self, property_name):
        if property_name not in self._config.keys():  # we don't want KeyError
            return None  # just return None if not found
        return self._config[property_name]
