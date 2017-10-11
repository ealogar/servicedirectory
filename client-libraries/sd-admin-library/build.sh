virtualenv ENV
source ENV/bin/activate
python setup.py install
pip install -r requirements_dev.txt
mkdir -p target/site/cobertura target/surefire-reports/
nosetests -s -v --with-cover --cover-package=com.tdigital.sd --cover-erase \
        --cover-branches --cover-xml-file=target/site/coverage.xml --cover-xml \
        --with-xunit --xunit-file=target/surefire-reports/TEST-nosetests.xml --nocapture
deactivate
