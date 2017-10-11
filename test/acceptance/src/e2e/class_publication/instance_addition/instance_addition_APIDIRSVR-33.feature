# -*- coding: utf-8 -*-
Feature: Instance Addition
  
  As a class provider
  I want to add and instance for my class
  so that it can be discovered by my consumers.

  @happy_path
  Scenario Outline: Addition of an instance with valid mandatory data_TDAFBA-470
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version                  | uri                                                                                                                                                             |
      | v                        | u                                                                                                                                                               |
      | v1.0                     | http://instance.tid.es                                                                                                                                          |
      | v57.12.12.110b-unstable  | http://instances.telefonica.com:22333/class/my%20instance%20in%20a%20url%20which%20is%20pretty%20long%20to%20check%20if%20that%20poses%20a%20problem%20or%20not |
      | [STRING_WITH_LENGTH_255] | under_boundary_value_version                                                                                                                                    |
      | [STRING_WITH_LENGTH_256] | boundary_value_version                                                                                                                                          |
      | under_boundary_value_url | [STRING_WITH_LENGTH_2047]                                                                                                                                       |
      | boundary_value_url       | [STRING_WITH_LENGTH_2048]                                                                                                                                       |
    Then I get a success response of type 201 with location <location_index>:
      | location                                                     |
      | $base_api_url/$classes_url/$class_name/$instances_url/(\w+)  |
    And the response contains the instance data
    And the location returns the instance data

    Examples: 
      | old_class_index | instance_index | location_index |
      | 0               | 0              | 0              |
      | 0               | 1              | 0              |
      | 0               | 2              | 0              |
      | 0               | 3              | 0              |
      | 0               | 4              | 0              |
      | 0               | 5              | 0              |
      | 0               | 6              | 0              |

  @happy_path
  Scenario Outline: Addition of an instance with valid mandatory and optional data_TDAFBA-471
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                     | environment                                                                           | attributes_keys                                                               | attributes_values                                                               |
      | v1.0    | http://instance1.tid.es | 1_sp                                                                                  | keytrue,keyfalse                                                              | True,False                                                                      |
      | v1.0    | http://instance2.tid.es | test:2                                                                                | key1,key2                                                                     | value,test                                                                      |
      | v1.0    | http://instance3.tid.es | production                                                                            | key3                                                                          | España                                                                          |
      | v1.0    | http://instance4.tid.es | integration                                                                           | long_key-name_in_case_it_is_started_to_be_filled_using_some_long_weird_format | DE                                                                              |
      | v1.0    | http://instance5.tid.es | Long_environment-name_in_case_it_is_started_to_be_filled_using_some_long_weird_format | key5                                                                          | Long_value-name_in_case_it_is_started_to_be_filled_using_some_long_weird_format |
      | v1.0    | http://instance6.tid.es | production                                                                            | [ARRAY_WITH_ITEMS_127]                                                        | [ARRAY_WITH_ITEMS_127]                                                   |
      | v1.0    | http://instance7.tid.es | production                                                                            | [ARRAY_WITH_ITEMS_128]                                                        | [ARRAY_WITH_ITEMS_128]                                                         |
      | v1.0    | http://instance8.tid.es | [STRING_WITH_LENGTH_512]                                                              | key1                                                                          | boundary_enviroment_value                                                       |
      | v1.0    | http://instance9.tid.es | [STRING_WITH_LENGTH_511]                                                              | key1                                                                          | under_boundary_enviroment_value                                                 |
    Then I get a success response of type 201 with location <location_index>:
      | location                                                     |
      | $base_api_url/$classes_url/$class_name/$instances_url/(\w+)  |
    And the response contains the instance data
    And the location returns the instance data

    Examples: 
      | old_class_index | instance_index | location_index |
      | 0               | 0              | 0              |
      | 0               | 1              | 0              |
      | 0               | 2              | 0              |
      | 0               | 3              | 0              |
      | 0               | 4              | 0              |
      | 0               | 5              | 0              |
      | 0               | 6              | 0              |
      | 0               | 7              | 0              |
      | 0               | 8              | 0              |

  @happy_path
  Scenario Outline: Addition of an instance with a new class_name which is ignored_TDAFBA-472
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | class_name | version | uri                    |
      | New_class  | v1.0    | http://instance.tid.es |
    # the new class_name is sent to the server, but not considered in the following steps
    Then I get a success response of type 201 with location <location_index>:
      | location                                                     |
      | $base_api_url/$classes_url/$class_name/$instances_url/(\w+)  |
    And the response contains the instance data
    And the location returns the instance data

    Examples: 
      | old_class_index | instance_index | location_index |
      | 0               | 0              | 0              |

  @happy_path
  Scenario Outline: Addition of instances with different mandatory and no values collision
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                     |
      | v1.0    | http://instance.tid.es  |
      | v1.0    | http://instance2.tid.es |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                           |
      | v2.0    | http://instance.tid.es        |
      | v1.0    | http://backup.instance.tid.es |
    Then I get a success response of type 201 with location <location_index>:
      | location                                                     |
      | $base_api_url/$classes_url/$class_name/$instances_url/(\w+)  |
    And the response contains the instance data
    And the location returns the instance data

    Examples: 
      | old_class_index | old_instance_index | instance_index | location_index |
      | 0               | 0                  | 0              | 0              |
      | 0               | 1                  | 1              | 0              |

  @method_not_allowed
  Scenario Outline: Publication of an instance with wrong method
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I try to put in $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri |
      | v       | u   |
    Then I get an error response of type 405 with error code SVC1003
    And the exceptionText contains <exceptionText_index>
      | exceptionText                           |
      | Requested Operation does not exist:(.*) |

    Examples: 
      | old_class_index | instance_index | exceptionText_index |
      | 0               | 0              | 0                   |

  @internal_error
  Scenario Outline: Addition of instances when the DB is down_TDAFBA-479
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And the DB has stopped working
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    Then I get an error response of type 500 with error code SVR1000
    And the exceptionText contains <exceptionText_index>:
      | exceptionText            |
      | Generic Server Error(.*) |

    Examples: 
      | old_class_index | instance_index | exceptionText_index |
      | 0               | 0              | 0                   |

  @malformed_request
  Scenario Outline: Publication of a new class using unstructured data_TDAFBA-467
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the data UNSTRUCTURED_DATA
    Then I get an error response of type 403 with error code POL0011
    And the exceptionText contains <exceptionText_index>:
      | exceptionText                                |
      | Media type (.*) not supported |

    Examples: 
      | old_class_index | exceptionText_index |
      | 0               | 0                   |

  @malformed_request
  Scenario Outline: Publication of a new class using malformed data
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the data MALFORMED_DATA
    Then I get an error response of type 400 with error code SVC1023
    And the exceptionText contains <exceptionText_index>
      | exceptionText                              |
      | Parser Error: (.*) content not well formed |

    Examples: 
      | old_class_index | exceptionText_index |
      | 0               | 0                   |

  @resource_not_found
  Scenario Outline: Addition of instances to a non existing class
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I send to $base_api_url/$classes_url/Class2/$instances_url the instance data <instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>:
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | instance_index | exceptionText_index |
      | 0               | 0              | 0                   |

  @missing_mandatory
  Scenario Outline: Addition of an instance with missing mandatory data
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version         | uri             |
      | [MISSING_PARAM] | http://a.test   |
      | v1.0            | [MISSING_PARAM] |
    Then I get an error response of type 400 with error code SVC1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText                    |
      | Missing mandatory parameter:(.*) |

    Examples: 
      | old_class_index | instance_index | exceptionText_index |
      | 0               | 0              | 0                   |
      | 0               | 1              | 0                   |

  @parameters_validation
  Scenario Outline: Addition of an instance with invalid mandatory (uri and version) data_TDAFBA-473
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version                  | uri                         |
      |                          | http://instance.tid.es      |
      | v1.0                     |                             |
      | No_string_instance       | 1                           |
      | 1.0                      | http://version_no_string    |
      | [STRING_WITH_LENGTH_257] | over_boundary_value_version |
      | over_boundary_value_url  | [STRING_WITH_LENGTH_2049]   |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                 |
      | Invalid parameter value: (.*) |

    Examples: 
      | old_class_index | instance_index | exceptionText_index |
      | 0               | 0              | 0                   |
      | 0               | 1              | 0                   |
      | 0               | 2              | 0                   |
      | 0               | 3              | 0                   |
      | 0               | 4              | 0                   |
      | 0               | 5              | 0                   |

  @existing_resource
  Scenario Outline: Addition of instances with the same mandatory data _TDAFBA-477
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                                                                       |
      | Invalid parameter value: Class-http://instance.tid.es-v1.0. Supported values are: non-duplicated-instance |

    Examples: 
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |

  @existing_resource
  Scenario Outline: Addition of instances with the same mandatory data and different optional data_TDAFBA-478
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v1.0    | http://instance.tid.es | integration | key1            | ES                |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v1.0    | http://instance.tid.es | production  | key1            | ES                |
      | v1.0    | http://instance.tid.es | integration | key2            | ES                |
      | v1.0    | http://instance.tid.es | integration | key1            | BR                |
      | v1.0    | http://instance.tid.es | production  | key5            | BR                |
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                                                |
      | Invalid parameter value: (.*). Supported values are: non-duplicated-instance |

    Examples: 
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |
      | 0               | 0                  | 1              | 0                   |
      | 0               | 0                  | 2              | 0                   |
      | 0               | 0                  | 3              | 0                   |

  @parameters_validation
  Scenario Outline: Addition of an instance with invalid optional data (attributes)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                     | environment | attributes_keys          | attributes_values            |
      | v1.1    | http://instance2.tid.es | production  |                          |                              |
      | v1.2    | http://instance2.tid.es | production  | key_empty_value          |                              |
      | v1.3    | http://instance2.tid.es | production  |                          | empty_key                    |
      | v1.4    | http://instance2.tid.es | production  | [MALFORMED]              | [MALFORMED]                  |
      | v1.5    | http://instance1.tid.es | production  | key_no_string            | 1                            |
      | v1.6    | http://instance1.tid.es | production  | key_int,key_string       | 1,a                          |
      | v1.7    | http://instance1.tid.es | production  | key_float                | 1.5                          |
      | v1.8    | http://instance1.tid.es | production  | key_boolean              | [TRUE]                       |
      | v1.9    | http://instance1.tid.es | production  | Key_in_classs            | Classs_in_attribute          |
      | v1.10   | http://instance1.tid.es | production  | [ARRAY_WITH_ITEMS_129]   | over_boundary_key |
      | v1.11   | http://instance1.tid.es | production  | [STRING_WITH_LENGTH_513] | over_boundary_key_attr       |
      | v1.12   | http://instance1.tid.es | production  | over_boundary_value_attr | [STRING_WITH_LENGTH_513]     |
    #     | v1.13    | http://instance1.tid.es | production  | key1 , [STRING_WITH_LENGTH_513]    | value1, over_boundary_key_attr  |
    #     | v1.14   | http://instance1.tid.es | production  |   key1, over_boundary_value_attr     |   value1 ,[STRING_WITH_LENGTH_513]  |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                 |
      | Invalid parameter value: (.*) |

    Examples: 
      | old_class_index | instance_index | location_index | exceptionText_index |
      | 0               | 0              | 0              | 0                   |
      | 0               | 1              | 0              | 0                   |
      | 0               | 2              | 0              | 0                   |
      | 0               | 3              | 0              | 0                   |
      | 0               | 4              | 0              | 0                   |
      | 0               | 5              | 0              | 0                   |
      | 0               | 6              | 0              | 0                   |
      | 0               | 7              | 0              | 0                   |
      | 0               | 8              | 0              | 0                   |
      | 0               | 9              | 0              | 0                   |
      | 0               | 10             | 0              | 0                   |
      | 0               | 11             | 0              | 0                   |

  #     | 0               | 12              | 0              | 0                   |
  #     | 0               | 13              | 0              | 0                   |
  @parameters_validation
  Scenario Outline: Addition of an instance with invalid optional data (duplicated attributes)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                     | environment | attributes_keys | attributes_values |
      | v1.0    | http://instance1.tid.es | production  | [REPEATED_KEY]  | ES,ES             |
    Then I get an error response of type 400 with error code SVC1023
    And the exceptionText contains <exceptionText_index>
      | exceptionText                              |
      | Parser Error: JSON content not well formed |

    Examples: 
      | old_class_index | instance_index | location_index | exceptionText_index |
      | 0               | 0              | 0              | 0                   |

  @parameters_validation
  Scenario Outline: Addition of an instance with invalid optional data (environment)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                                    | environment              |
      | v1.0     | http://environment_empty               |                          |
      | v1.0     | http://environment_no_string           | 2                        |
      | v1.0     | http://over_boundary_value_environment | [STRING_WITH_LENGTH_513] |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                 |
      | Invalid parameter value: (.*) |

    Examples: 
      | old_class_index | instance_index | location_index | exceptionText_index |
      | 0               | 0              | 0              | 0                   |
      | 0               | 1              | 0              | 0                   |
      | 0               | 2              | 0              | 0                   |
