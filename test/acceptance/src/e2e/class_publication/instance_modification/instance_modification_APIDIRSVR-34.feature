# -*- coding: utf-8 -*-
Feature: Endpoint Modification
  
  As a class provider
  I would like to be able to modify the instances that are being exposed by the Service Director
  So that I can update them when it is necessary

  @happy_path
  Scenario Outline: Modification of an instance with valid mandatory data_TDAFBA-480
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v1.0     | http://instance.tid.es | integration |
      | v1.1     | http://instance.tid.es | integration |
      | v1.2     | http://instance.tid.es | integration |
      | v1.3     | http://instance.tid.es | integration |
      | v1.4     | http://instance.tid.es | integration |
      | v1.5     | http://instance.tid.es | integration |
      | v1.6     | http://instance.tid.es | integration |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | version                  | uri                                                                                                                                                             |
      | v                        | u                                                                                                                                                               |
      | v1.0                     | http://instance.tid.es                                                                                                                                          |
      | v57.12.12.110b-unstable  | http://instances.telefonica.com:22333/class/my%20instance%20in%20a%20url%20which%20is%20pretty%20long%20to%20check%20if%20that%20poses%20a%20problem%20or%20not |
      | [STRING_WITH_LENGTH_255] | under_boundary_value_version                                                                                                                                    |
      | [STRING_WITH_LENGTH_256] | boundary_value_version                                                                                                                                          |
      | under_boundary_value_url | [STRING_WITH_LENGTH_2047]                                                                                                                                       |
      | boundary_value_url       | [STRING_WITH_LENGTH_2048]                                                                                                                                       |
    Then I get a success response of type 200 with the updated instance data
    And the URL $base_api_url/$classes_url/$class_name/$instances_url/$instance_id returns the updated instance data

    Examples: 
      | old_class_index | old_instance_index | instance_index |
      | 0               | 0                  | 0              |
      | 0               | 1                  | 1              |
      | 0               | 2                  | 2              |
      | 0               | 3                  | 3              |
      | 0               | 4                  | 4              |
      | 0               | 5                  | 5              |
      | 0               | 6                  | 6              |

  @happy_path
  Scenario Outline: Modification of an instance with valid mandatory and optional data_TDAFBA-481
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                     | environment | attributes_keys | attributes_values |
      | v0.0    | http://instance0.tid.es | 0_sp        | key_0,key_0     | False,True        |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | version | uri                     | environment                                                                           | attributes_keys                                                               | attributes_values                                                               |
      | v1.0    | http://instance1.tid.es | 1_sp                                                                                  | keytrue,keyfalse                                                              | True,False                                                                      |
      | v1.0    | http://instance2.tid.es | test:2                                                                                | key1,key2                                                                     | value,test                                                                      |
      | v1.0    | http://instance3.tid.es | production                                                                            | key3                                                                          | España                                                                          |
      | v1.0    | http://instance4.tid.es | integration                                                                           | long_key-name_in_case_it_is_started_to_be_filled_using_some_long_weird_format | DE                                                                              |
      | v1.0    | http://instance5.tid.es | Long_environment-name_in_case_it_is_started_to_be_filled_using_some_long_weird_format | key5                                                                          | Long_value-name_in_case_it_is_started_to_be_filled_using_some_long_weird_format |
      | v1.0    | http://instance6.tid.es | production                                                                            | [ARRAY_WITH_ITEMS_127]                                                        | under_boundary_num_attributes                                                   |
      | v1.0    | http://instance7.tid.es | production                                                                            | [ARRAY_WITH_ITEMS_128]                                                        | boundary_num_attributes                                                         |
      | v1.0    | http://instance8.tid.es | [STRING_WITH_LENGTH_512]                                                              | key1                                                                          | boundary_enviroment_value                                                       |
      | v1.0    | http://instance9.tid.es | [STRING_WITH_LENGTH_511]                                                              | key1                                                                          | under_boundary_enviroment_value                                                 |
    Then I get a success response of type 200 with the updated instance data
    And the URL $base_api_url/$classes_url/$class_name/$instances_url/$instance_id returns the updated instance data

    Examples: 
      | old_class_index | old_instance_index | instance_index |
      | 0               | 0                  | 0              |
      | 0               | 0                  | 1              |
      | 0               | 0                  | 2              |
      | 0               | 0                  | 3              |
      | 0               | 0                  | 4              |
      | 0               | 0                  | 5              |
      | 0               | 0                  | 6              |
      | 0               | 0                  | 7              |
      | 0               | 0                  | 8              |

  @happy_path
  Scenario Outline: Modification of an instance adding optional data that was not there_TDAFBA-482
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v1.0    | http://instance.tid.es | integration | key_0,key_0     | False,True        |
    Then I get a success response of type 200 with the updated instance data
    And the URL $base_api_url/$classes_url/$class_name/$instances_url/$instance_id returns the updated instance data

    Examples: 
      | old_class_index | old_instance_index | instance_index |
      | 0               | 0                  | 0              |
      
  @happy_path
  Scenario Outline: Modification of an instance modifying few values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v1.0    | http://instance.tid.es | integration | key_0,key_0     | False,True        |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | version | uri                    | 
      | v1.2    | http://instance.tid2.es | 
    Then I get a success response of type 200 with the updated instance data
    And the URL $base_api_url/$classes_url/$class_name/$instances_url/$instance_id returns the updated instance data

    Examples: 
      | old_class_index | old_instance_index | instance_index |
      | 0               | 0                  | 0              |

  @happy_path
  Scenario Outline: Modification of an instance with a new class_name which is ignored_TDAFBA-483
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v1.0    | http://instance.tid.es | integration |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | class_name | version | uri                           |
      | New_class  | v2.0    | http://backup.instance.tid.es |
    # the new class_name is sent to the server, but not considered in the following steps
    Then I get a success response of type 200 with the updated instance data
    And the URL $base_api_url/$classes_url/$class_name/$instances_url/$instance_id returns the updated instance data

    Examples: 
      | old_class_index | old_instance_index | instance_index |
      | 0               | 0                  | 0              |

  @method_not_allowed
  Scenario Outline: Partial update of an instance
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    When I try to partially update in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | version | uri |
      | v       | u   |
    Then I get an error response of type 405 with error code SVC1003
    And the exceptionText contains <exceptionText_index>
      | exceptionText                           |
      | Requested Operation does not exist:(.*) |

    Examples: 
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |

  @internal_error
  Scenario Outline: Modification of an instance when the DB is down_TDAFBA-489
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the DB has stopped working
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | version | uri                           |
      | v2.0    | http://backup.instance.tid.es |
    Then I get an error response of type 500 with error code SVR1000
    And the exceptionText contains <exceptionText_index>:
      | exceptionText            |
      | Generic Server Error(.*) |

    Examples: 
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |

  @malformed_request
  Scenario Outline: Modification of an instance using unstructured data_TDAFBA-467
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the data UNSTRUCTURED_DATA
    Then I get an error response of type 403 with error code POL0011
    And the exceptionText contains <exceptionText_index>:
      | exceptionText                                |
      | Media type (.*) not supported |

    Examples: 
      | old_class_index | old_instance_index | exceptionText_index |
      | 0               | 0                  | 0                   |

  @malformed_request
  Scenario Outline: Modification of an instance using malformed data
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the data MALFORMED_DATA
    Then I get an error response of type 400 with error code SVC1023
    And the exceptionText contains <exceptionText_index>
      | exceptionText                              |
      | Parser Error: (.*) content not well formed |

    Examples: 
      | old_class_index | old_instance_index | exceptionText_index |
      | 0               | 0                  | 0                   |

  @resource_not_found
  Scenario Outline: Modification of a non existing instance of a non existing class
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has not already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v1.0    | http://instance.tid.es | integration |
    When I put in $base_api_url/$classes_url/Non_existing_Class/$instances_url/$instance_id the instance data <instance_index>:
      | version | uri                           |
      | v2.0    | http://backup.instance.tid.es |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>:
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |

  @resource_not_found
  Scenario Outline: Modification of an instance not already published_TDAFBA-487
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has not already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v1.0    | http://instance.tid.es | integration |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | version | uri                           |
      | v2.0    | http://backup.instance.tid.es |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>:
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |

  @resource_not_found
  Scenario Outline: Modification of an instance over an non existing class and existing instance
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has not already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v1.0    | http://instance.tid.es | integration |
    When I put in $base_api_url/$classes_url/Non_existing_Class/$instances_url/$instance_id the instance data <instance_index>:
      | version | uri                           |
      | v2.0    | http://backup.instance.tid.es |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>:
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |

  @resource_not_found
  Scenario Outline: Modification of an existing instance and existing class but not related
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0     | http://instance.tid.es |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class2     | Class       | v1.0             |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | version | uri                           |
      | v2.0    | http://backup.instance.tid.es |
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>:
      | exceptionText                |
      |Invalid parameter value: (.*). Supported values are: (.*) |

    Examples: 
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |

  @missing_mandatory
  Scenario Outline: Modification of an instance with missing mandatory data
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class1     | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                        |
      | v0.0    | http://instance_olf.tid.es |
      | v0.1    | http://instance_olf.tid.es |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | version         | uri             |
      | [MISSING_PARAM] | http://a.test   |
      | v1.0            | [MISSING_PARAM] |
    Then I get an error response of type 400 with error code SVC1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText                    |
      | Missing mandatory parameter:(.*) |

    Examples: 
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |
      | 0               | 1                  | 1              | 0                   |

  @parameters_validation
  Scenario Outline: Modification of an instance with invalid mandatory (uri and version) data_TDAFBA-473
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                        |
      | v0.1    | http://instance_old.tid.es |
      | v0.2    | http://instance_old.tid.es |
      | v0.3    | http://instance_old.tid.es |
      | v0.4    | http://instance_old.tid.es |
      | v0.5    | http://instance_old.tid.es |
      | v0.6    | http://instance_old.tid.es |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
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
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |
      | 0               | 1                  | 1              | 0                   |
      | 0               | 2                  | 2              | 0                   |
      | 0               | 3                  | 3              | 0                   |
      | 0               | 4                  | 4              | 0                   |
      | 0               | 5                  | 5              | 0                   |

  @existing_resource
  Scenario Outline: Modification of an instance matching another existing instance_TDAFBA-488
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v1.0    | http://instance.tid.es | integration |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                           | environment |
      | v2.0    | http://backup.instance.tid.es | production  |
    # next steps execute over the last instance created (not the first one)
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | version | uri                    | environment |
      | v1.0    | http://instance.tid.es | integration |
      | v1.0    | http://instance.tid.es | production  |
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                                                                       |
      | Invalid parameter value: Class-http://instance.tid.es-v1.0. Supported values are: non-duplicated-instance |

    Examples: 
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |
      | 0               | 0                  | 1              | 0                   |

  @parameters_validation
  Scenario Outline: Modification of an instance with invalid optional data (attributes)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                     | environment | attributes_keys | attributes_values |
      | v0.0    | http://instance0.tid.es | integration | old_key         | old_value         |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | version | uri                     | environment | attributes_keys          | attributes_values            |
      | v1.1    | http://instance2.tid.es | production  |                          |                              |
      | v1.2    | http://instance2.tid.es | production  | key_empty_value          |                              |
      | v1.3    | http://instance2.tid.es | production  |                          | Empty_key                    |
      | v1.4    | http://instance2.tid.es | production  | [MALFORMED]              | [MALFORMED]                  |
      | v1.5    | http://instance1.tid.es | production  | key_no_string            | 1                            |
      | v1.6    | http://instance1.tid.es | production  | key_int,key_string       | 1,a                          |
      | v1.7    | http://instance1.tid.es | production  | key_float                | 1.5                          |
      | v1.8    | http://instance1.tid.es | production  | key_boolean              | [TRUE]                       |
      | v1.9    | http://instance1.tid.es | production  | Key_in_classs            | Classs_in_attribute          |
      | v1.10   | http://instance1.tid.es | production  | [ARRAY_WITH_ITEMS_129]   | over_boundary_num_attributes |
      | v1.11   | http://instance1.tid.es | production  | [STRING_WITH_LENGTH_513] | over_boundary_key_attr       |
      | v1.12   | http://instance1.tid.es | production  | over_boundary_value_attr | [STRING_WITH_LENGTH_513]     |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                 |
      | Invalid parameter value: (.*) |

    Examples: 
      | old_class_index | old_instance_index | instance_index | location_index | exceptionText_index |
      | 0               | 0                  | 0              | 0              | 0                   |
      | 0               | 0                  | 1              | 0              | 0                   |
      | 0               | 0                  | 2              | 0              | 0                   |
      | 0               | 0                  | 3              | 0              | 0                   |
      | 0               | 0                  | 4              | 0              | 0                   |
      | 0               | 0                  | 5              | 0              | 0                   |
      | 0               | 0                  | 6              | 0              | 0                   |
      | 0               | 0                  | 7              | 0              | 0                   |
      | 0               | 0                  | 8              | 0              | 0                   |
      | 0               | 0                  | 9              | 0              | 0                   |
      | 0               | 0                  | 10             | 0              | 0                   |
      | 0               | 0                  | 11             | 0              | 0                   |

  @parameters_validation
  Scenario Outline: Modification of an instance with invalid optional data (duplicated attributes)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                     | environment | attributes_keys | attributes_values |
      | v0.0    | http://instance0.tid.es | integration | old_key         | old_value         |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/$instance_id the instance data <instance_index>:
      | version | uri                     | environment | attributes_keys | attributes_values |
      | v1.0    | http://instance1.tid.es | production  | [REPEATED_KEY]  | ES,ES             |
    Then I get an error response of type 400 with error code SVC1023
    And the exceptionText contains <exceptionText_index>
      | exceptionText                              |
      | Parser Error: JSON content not well formed |

    Examples: 
      | old_class_index | old_instance_index | instance_index | location_index | exceptionText_index |
      | 0               | 0                  | 0              | 0              | 0                   |

  @parameters_validation
  Scenario Outline: Modification of an instance with invalid optional data (environment)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                     | environment | attributes_keys | attributes_values |
      | v0.0    | http://instance0.tid.es | integration | old_key         | old_value         |
      | v0.1    | http://instance0.tid.es | integration | old_key         | old_value         |
      | v0.2    | http://instance0.tid.es | integration | old_key         | old_value         |
    When I put in $base_api_url/$classes_url/$class_name/$instances_url/instance_id the instance data <instance_index>:
      | version | uri                                    | environment              |
      | v1.0     | http://environment_empty               |                          |
      | v1.0     | http://environment_no_string           | 2                        |
      | v1.0     | http://over_boundary_value_environment | [STRING_WITH_LENGTH_513] |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                 |
      | Invalid parameter value: (.*) |

    Examples: 
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |
      | 0               | 1                  | 1              | 0                   |
      | 0               | 2                  | 2              | 0                   |
