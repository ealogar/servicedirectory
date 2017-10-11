# Simple library to use the service directory

## Overview
It provides an internal caching system based on memoization to return endpoints quickly

Everything can be configurable, you may read the docstring for further info

You can see the unit tests also if you need aditional infor on using the library

## Usage

Prerequisites in requirements.txt, you can instal them as follow
```python
pip install -r requirements.txt
```

You can use the library directly with constructor:
```python
from com.tdigital.sd.sd_discovery import ServiceDirectory
library = ServiceDirectory('demo-tdafsd-ws-01', 8000, 'v1', ttl=55, ttr=360, timeout=30)
endpoints = library.get_endpoints('Sprayer2', 'production')
```

Alternativelly, you can provide a service-directory.properties file in any directory inside pythonpath

A value in constructor take priority against value in properties

If a value is not given in constructor or properties, it will take a default value
ttl=1 week, ttr = 1 hour, timeout = 30 seconds and last version obtained from sd
library = ServiceDirectory('demo-tdafsd-ws-01', 8000)

get_endpoints returns a list of Endpoint objects with direct access to properties:

api_name, version, url, environment, endpoint_attributes
first_url_available = endpoints[0].url

you can provide custom search criteria for api and get default values

```python
endpoints = library.get_endpoints('Sprayer2', 'production', opt_query_parameters={'ob': 'ES'})
```

You can use the behaviour param and provide the api version

```python
try:
    endpoints = library.get_endpoints('Sprayer2', 'production', api_version='1.0', behaviour='param_check_strict',
                                opt_query_parameters={'non_existing_param': 'some_value'})
except SDLibraryException as e:
    print str(e)
```

In order to run the tests run the following command from this directory

```sh
nosetests --with-coverage --cover-erase --cover-package=com.tdigital.sd --cover-html
```
