# -*- coding: utf-8 -*-
Feature: Logging Mechanism
  
    As an operation manager (O&M)
    I want that any relevant event is registered in log files according to a well defined pattern
    So that I can extract and filter the Information of interest with a common toolset.

  Scenario: Log the unica correlator received
    Given the DB has no classes already published
    When I send to $base_api_url/$classes_url the class data with unica_correlator example_of_correlator_32_chars__:
      | default_version | class_name |
      | v1.0             | Class      |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR                      | LEVEL    | MESSAGE                                           |
      | op=CreateClass | trans=.{32,}   | corr=example_of_correlator_32_chars__ | lvl=INFO | msg=(.*) Error in request with code SVC1019: (.*) |
    And unica_correlator example_of_correlator_32_chars__ is returned in the response

  Scenario: Log when a client makes a request with data not supported
    #SD-CORE-9
    Given the DB has no classes already published
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the data UNSTRUCTURED_DATA
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code POL0011: (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario Outline: Log when a bound isntance has been deleted
    #SD-CORE-20
    Given the DB has no classes already published
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data:
      | class_name | description | default_version |
      | Class      | New class   | v1.0             |
    And an instance has already been published with data:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available:
      | operation | input_context_param | value |
      | regex     | version             | (.*)  |
    And the previous bindings are published for the context:
      | origin  | class_name |
      | Client0 | Class      |
    And the instance published in position 0 has been deleted
    When I request the resource $base_api_url/$bind_instances_url with parameters:
      | version | class_name | origin  |
      | v2.0    | Class      | Client0 |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE         | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=BindServiceInstance | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC2003: (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when the initial connection to the DB cannot be established
    # SD-CORE-1
    Given the DB has stopped working
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I restart the Service Directory
    And I send to $base_api_url/$classes_url the class data:
      | class_name | default_version |
      | Class      | v1.0             |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL     | MESSAGE                                                                     |
      | op=NA          | trans=.{32,}   | corr=.{32,}      | lvl=FATAL | msg=(.*) It has not been possible to start the connection to the hosts (.+) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when a request to the DB fails
    #SD-CORE-2
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data:
      | class_name | description | default_version |
      | Class_old  | class       | v1.0             |
    And the DB has stopped working
    When I send to $base_api_url/$classes_url the class data:
      | class_name | default_version |
      | Class    | v1.0             |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                                               |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=WARN | msg=(.*) Operation failed, trying another time \[(\d+) of (\d+)\] |
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL     | MESSAGE                                                    |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=ERROR | msg=(.*) Operation failed permanently after (\d+) retries |
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL     | MESSAGE                                                                 |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=ERROR | msg=(.*) Error in request with code SVR1000: Generic Server Error: (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when a client makes a request to an nonexisting resource (Django exception)
    #SD-CORE-6
    Given the DB has no classes already published
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url/wrong_path the class data:
      | class_name | default_version |
      | Class      | v1.0             |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=UpdateClass | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC1006: (.+) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when a client makes a request to an nonexisting resource (SD exception)
    #SD-CORE-6
    Given the DB has no classes already published
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data:
      | class_name | description | default_version |
      | Class_old  | class       | v1.0             |
    When I send to $base_api_url/$classes_url/Non_existing_Class/$instances_url the instance data:
      | version | uri |
      | v       | u   |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE    | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=CreateInstance | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC1006: (.+) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when a a request is sent with a bad parameter and other options are presented
    #SD-CORE-7
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data:
      | class_name | default_version |
      | Class      | v1.0             |
    When I send to $base_api_url/$classes_url the class data:
      | class_name | default_version |
      | Class      | v1.0             |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC1021: (.+) |
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                                          |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Invalid parameter value:(.*). Supported values are:(.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when a client makes a request with invalid data
    #SD-CORE-8
    Given the DB has no classes already published
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data:
      | class_name | description | default_version |
      | Class_old  | class       | v1.0             |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data:
      | version | uri |
      | 1.0     | u   |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE    | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=CreateInstance | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC0002: (.+) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when you have invalid credentials
    #SD-CORE-10
    Given the DB has no classes already published
    Given the user performing the operation is:
      | username | password |
      | admin    | invalid  |
    When I send to $base_api_url/$classes_url the class data:
      | class_name | default_version |
      | Class      | v1.0             |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC1018: (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when user has no privileges to access resource
    #SD-CORE-11
    Given the DB has no classes already published
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a user has already been created with data:
      | username    | password    | is_admin |
      | other_admin | other_admin | [FALSE]    |
    And the user performing the operation is:
      | username    | password    |
      | other_admin | other_admin |
    When I request a resource $base_api_url/$users_url
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=ListUsers   | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC1013: (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when operation not allowed
    #SD-CORE-12
    Given the DB has no classes already published
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I try to put in $base_api_url/$classes_url the class data:
      | class_name | description | default_version |
      | Class      | class       | v1.0             |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE                    | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=PUT-ServiceClassCollectionView | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC1003: (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when the default admin credentials cannot be found in the config file
    #SD-CORE-14
    Given the config file does not contain the default admin credentials
    And I restart the Service Directory
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data:
      | class_name | default_version |
      | Class      | v1.0             |
    When I send to $base_api_url/$classes_url the class data:
      | class_name | default_version |
      | Class      | v1.0             |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL     | MESSAGE                                                |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=ERROR | msg=(.*) Default admin credentials not found in config |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when missing mandatory param is no included in request
    #SD-CORE-16
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data:
      | default_version |
      | v1.0             |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC1000: (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when a parameter is invalid
    #SD-CORE-18
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters:
      | nokey |
      | nokey |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE     | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=SearchInstances | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC1001: (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when a request is done with an invalid value
    #SD-CORE-21
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data:
      | class_name | default_version |
      | Class.     | v1.0             |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC0002: (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when a request with unsupported type has been performed
    #SD-CORE-29
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And the DB has no classes already published
    When I send to $base_api_url/$classes_url the data UNSTRUCTURED_DATA
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code POL0011: (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when you have not supplied credentials over a resource that requires them
    #SD-CORE-30
    Given the DB has no classes already published
    And no authentication method is provided
    When I send to $base_api_url/$classes_url the class data:
      | class_name | default_version |
      | Class      | v1.0             |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC1019: (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario Outline: Log when no default rules are defined for class
    #SD-CORE-19
    Given the DB has no classes already published
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data:
      | class_name | description | default_version |
      | Class      | New class   | v1.0             |
    And an instance has already been published with data:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available:
      | operation | input_context_param | value |
      | regex     | version             | (.*)  |
    And the previous bindings are published for the context:
      | origin  | class_name |
      | Client0 | Class      |
    When I request the resource $base_api_url/$bind_instances_url with parameters:
      | version | class_name |
      | v2.0    | Class      |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE         | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                           |
      | op=BindServiceInstance | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Error in request with code SVC2002: (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when json schemas are not found
    #SD-CORE-31
    Given the json schemas are missing
    And I restart the Service Directory
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data:
      | default_version | class_name |
      | v1.0             | Class      |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL     | MESSAGE                                           |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=FATAL | msg=(.*) The json schema ClassModel is not found. |
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL     | MESSAGE                                                                 |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=ERROR | msg=(.*) Error in request with code SVR1000: Generic Server Error: (.*) |

  Scenario: Log when json schemas folder is not found
    #SD-CORE-31
    Given the json schemas folder is missing
    And I restart the Service Directory
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data:
      | default_version | class_name |
      | v1.0             | Class      |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL     | MESSAGE                                           |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=FATAL | msg=(.*) The json schema ClassModel is not found. |
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL     | MESSAGE                                                                 |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=ERROR | msg=(.*) Error in request with code SVR1000: Generic Server Error: (.*) |

  Scenario: Log when the correlator header cannot be found in the config file
    #SD-CORE-32
    Given the config file does not contain the correlator header
    And I restart the Service Directory
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data:
      | class_name | default_version |
      | Class      | v1.0             |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL     | MESSAGE                                                   |
      | op=NA          | trans=NA       | corr=NA          | lvl=ERROR | msg=(.*) Unica Correlator headers not defined in settings |

  Scenario: Log when a request with Json not valid is performed
    #SD-CORE-27
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data:
      | class_name | description | default_version |
      | Class      | New class   | v1.0             |
    And an instance has already been published with data:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available:
      | operation | input_context_param | value      |
      | eq        | test                | [BAD_JSON] |
    When I send to $base_api_url/$bindings_url the rule data:
      | origin  | class_name |
      | Client0 | Class      |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE      | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL    | MESSAGE                                                             |
      | op=CreateClassRules | trans=.{32,}   | corr=.{32,}      | lvl=INFO | msg=(.*) Object not compliant with schema validation for Model (.*) |
    And unica_correlator .{32,} is returned in the response

  Scenario: Log when validation of user can not be done with mongo
    #SD-CORE-15 (Deletes database)
    Given the DB has no classes already published
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a user has already been created with data:
      | username    | password    | is_admin |
      | other_admin | other_admin | [TRUE]     |
    And the user performing the operation is:
      | username    | password    |
      | other_admin | other_admin |
    And the passwords have been deleted
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data:
      | default_version | class_name |
      | v1.0             | Class      |
    Then the format of the logs is correct
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL     | MESSAGE                                                     |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=ERROR | msg=authentication: Error in authenticate method u'password' |
    And I see in the logs an entry with the following data:
      | OPERATION_TYPE | TRANSACTION_ID | UNICA_CORRELATOR | LEVEL     | MESSAGE                                                                 |
      | op=CreateClass | trans=.{32,}   | corr=.{32,}      | lvl=ERROR | msg=(.*) Error in request with code SVR1000: Generic Server Error: (.*) |
    And the users DB is restored
    And unica_correlator .{32,} is returned in the response
