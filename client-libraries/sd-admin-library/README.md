# Library and CLI to manage and operate the service directory

## Overview
This library exposes all the capabilities of the service directory beyond the binding instances 
provided by sd-python-library.
It also provides a CLI (command-line interface) to operate the service directory remotely.

## Usage

To install the library and CLI, execute:
```bash
sudo python setup.py install
```

For development, you must install requirements_dev.txt as well:
```bash
sudo pip install -r requirements_dev.txt
```

The installer will create the python egg in default directory (library and CLI), a configuration file (cli.conf located inside egg), and a script to launch the CLI (sd-cli) available in the PATH.

The capabilities implemented by the admin library are distributed into the following modules:
* info.py. To get basic information about the service directory
* classes.py. To manage Service Classes
* instances.py. To manage service instances)
* bindings.py. To manage client rules (to customize the search for endpoints)

Any of these python modules require a "Client" object to interact with the service directory. This object handles the HTTP requests and responses, as well as the JSON documents. It also configures the security (HTTPS and 2-way SSL are supported).

The following example creates a Client object and sends a Info request.

```python
from com.tdigital.sd.admin.client import Client
from com.tdigital.sd.admin.info import Info

client = Client(url='http://sd-host/sd/v1/', username='admin', password='admin')
info = Info(client)
print info.info()
```

The next example creates an instance. The client object establishes a 2-way SSL connection with the service directory:

```python
from com.tdigital.sd.admin.client import Client
from com.tdigital.sd.admin.instances import Instances

cert = ('/path/to/cert', '/path/to/key')
client = Client(url='https://sd-host/sd/v1/', username='admin', password='admin', cert=cert)
instances = Instances(client)
response = instances.create('fake', 'v1.0', 'production', 'http://fakeapi/fake/v1')
```

In order to run the tests, run the following command:

```sh
nosetests --with-coverage --cover-erase --cover-package=com.tdigital.sd --cover-html
```
