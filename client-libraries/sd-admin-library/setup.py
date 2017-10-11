'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from os.path import dirname, join, normpath, abspath
from os import chdir, pardir
from sys import prefix
from setuptools import setup, find_packages
from distutils.command.install import INSTALL_SCHEMES

try:
    with open(join(dirname(__file__), 'README.md')) as f:
        README = f.read()
except IOError:
    README = ''


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
chdir(normpath(join(abspath(__file__), pardir)))

# Change data default path to lib path
#for scheme in INSTALL_SCHEMES.values():
#    scheme['data'] = scheme['purelib']

setup(
    name='sd-admin-library',
    version='v1',
    packages=find_packages('src'),
    package_dir={'': ''},
    data_files=[('sd-config', [join('config', 'cli.conf')])],
    entry_points={
                'console_scripts': [
                    'sd-cli = com.tdigital.sd.cli.cli:command',
                ]
            },
    install_requires=get_requirements(),
    license='(C) Telefonica I+D',  # example license
    description='CLI library to manage and operate all the entities of the service directory via HTTP',
    long_description=README,
    url='http://www.tid.es',
    zip_safe=False,  # We need that config file can be readen from inside package
    author='Telefonica I+D',
    author_email='jorgelg@tid.es, eag@tid.es',
    classifiers=[
        'Environment :: CLI',
        'Framework :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Commercial',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
)
