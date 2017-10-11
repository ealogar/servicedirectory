#!/bin/bash
virtualenv-2.7 ENV
source ENV/bin/activate
pip install -r requirements.txt
pip install mock nose nose-cov
mkdir -p target/site/cobertura target/surefire-reports
rm -Rf target/site/cobertura/*.* target/surefire-reports/*.*
nosetests -s -v --with-cover --cover-package=com.tdigital --cover-erase \
        --cover-branches --cover-xml-file=target/site/cobertura/coverage.xml --cover-xml \
        --with-xunit --xunit-file=target/surefire-reports/TEST-nosetests.xml
