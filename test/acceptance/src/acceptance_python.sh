#!/bin/bash
# sh file to execute the python tests

python lettucetdaf.py --testsuite $1 --environment $2

exit $?
