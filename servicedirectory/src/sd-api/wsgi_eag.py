'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''

# http://jessenoller.com/2009/07/24/django-mod_wsgi-apache-and-os-x-do-it/
# http://stackoverflow.com/questions/12240289/mountainlion-apr-compile-lacking-cc
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.eag")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
