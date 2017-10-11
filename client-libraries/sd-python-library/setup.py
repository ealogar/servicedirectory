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

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

def get_requirements():
    reqs_file = 'requirements.txt'
    try:
        with open(reqs_file) as reqs_file:
            reqs = filter(None, map(lambda line: line.replace('\n', '').strip(), reqs_file))
            return reqs
    except IOError:
        pass
    return []

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='sd-library',
    version='v1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license='(C) Telefonica I+D',  # example license
    description='Service Directory API for easy searchs (with internal cache).',
    long_description=README,
    install_requires=get_requirements(),
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
