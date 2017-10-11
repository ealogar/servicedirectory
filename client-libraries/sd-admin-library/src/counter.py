'''
Created on 10/10/2013

@author: eag
'''
from argparse import ArgumentParser
from os.path import exists, isdir, join
from os import walk

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()
    top_dir = args.file
    if not exists(top_dir):
        print "{} does not exists".format(top_dir)
    print "about to count the lines of unit tests in base dir {0}".format(top_dir)
    if not isdir(top_dir):
        print "{} should be a directory".format(top_dir)
    TOTAL_LINES_TEST = 0
    for root, dirs, files in walk(top_dir):
        if root.endswith('tests'):
            for test_file in files:
                py_file = join(root, test_file)
                if py_file.endswith('.py'):
                    with open(py_file) as f:
                        for i, line in enumerate(f):
                            if line.strip() != '':
                                TOTAL_LINES_TEST += 1

    print "{} lines of test code".format(TOTAL_LINES_TEST)