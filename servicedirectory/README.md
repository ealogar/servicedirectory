# python-api-service-directory

## Requirements
See requirements.txt in order to install all required libraries using pip (preferred and most suitable way)
or an alternative system (easy_install).

Python minimum version required is 2.6.6+ 

It won't work with Python 3.0

## Installation

Configure a virtual environment with the required packages:

```
virtualenv ENV
source ENV/bin/activate
pip install -r requirements.txt
```

Then create the local database if you are using a local database for testing:

```
python manage.py syncdb
```

## Running tests

Run the service unit tests:

```
pip install -r requirements-test.txt
python manage.py test apis commons
```

## Running server

Run the service in the django development server:

```
python manage.py runserver
```

Now open the browser pointing to http://localhost:8000/sd/v1/apis/
