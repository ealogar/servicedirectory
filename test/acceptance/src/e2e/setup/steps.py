# -*- coding: utf-8 -*-
'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from lettuce import step, world
import requests


@step(u'Then I get the correct version of Mongo and Django')
def then_i_get_the_correct_version_of_mongo_and_django(step):
    if not world.mongo_is_up():
        world.start_mongo()   # make sure the DB is up before checking its version

    assert world.status_code == requests.codes.ok, "Response is not 200 OK"
    mongo_version = world.get_mongo_version()
    django_version = world.get_django_version()
    try:
        received_mongo_version = world.json["mongo_version"]
        received_django_version = world.json["django_version"]
    except:
        assert False, "Error getting the versions in the json"
    assert received_mongo_version == mongo_version, \
        "Mongo version received %s instead of %s" \
        % (received_mongo_version, mongo_version)
    assert received_django_version == django_version, \
        "Django version received %s instead of %s" \
        % (received_django_version, django_version)
