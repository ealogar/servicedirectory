'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
import os
from setuptools import setup, find_packages

#README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# find packages
_packages = map(lambda x: 'sd-api.{0}'.format(x), find_packages('sd-api'))
_packages = filter(lambda x: x.find('.test')==-1, _packages)
_packages.append('sd-api')

setup(
    name='service-directory',
    version='1.0.0',
    packages=_packages,
    package_data = {'': ['static/rest_framework/js/*', 
                         'static/rest_framework/css/*',
                         'static/rest_framework/img/*',
                         'schemas/*.json']},
    license='(C) Telefonica I+D',  # example license
    description='DNS for retrieving endpoints.',
    long_description='README',
    url='http://www.tid.es',
    author='Telefonica I+D',
    author_email='eag@tid.es',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
