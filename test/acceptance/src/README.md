Installation Instructions
-------------------------

* Install the python modules in requirements.txt in the execution environment: pip install -r requirements.txt
* Install the jirasync module from the tdaf-testcomponents auxiliary project, downloading it from the pdihub repository and using its setup.py: python setup.py install

Tests Execution Instructions
----------------------------

* Run lettucetdaf.py in this folder to execute the tests defined in the .features files (run with the -h option to see details of the different execution modes). 
* **Beware**: the acceptance tests are not meant to be run on production environments, as they make significant changes on the service that would result in data loss, service interruption, etc.

Jirasync Instructions
---------------------

* Just to synchronize the tests cases with Jira, run jirasync.py in this folder passing as only parameter the folder to go through looking for the .feature files to be synchronized with Jira.
