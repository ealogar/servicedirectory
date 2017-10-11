"""
Test modules should be named:
    tests_<module_to_be_tested>.py
    Ex:
       tests_services.py
"""
import glob
import os


# code to test selection
def get_tests(dirname):
    tests = [os.path.basename(f)[:-3] for f in glob.glob(os.path.join(dirname, "tests_*.py"))]
    enabled_modules = []
    for test in tests:
        tokens = test.split("_")
        module = ".".join(dirname.split(os.path.sep)[-2:]) + "." + test
        enabled_modules.append(__import__(module, globals(), locals(), ['*']))

    return enabled_modules
