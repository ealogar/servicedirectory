# -*- coding: utf-8 -*-
Feature: Rule publication
  
  As an operation manager
  I want to define rules associated to a context in order to bind them different instances
  So that I can modified the instances discovery according to my needs

  @missing_resource
  Scenario Outline: Binding publication over non existing class
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value   |
      | range     | uidd                | 100,200 |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name    |
      | Origin0 | Another_Class |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |

  @missing_resource
  Scenario Outline: Binding publication without mandatory origin and class
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value   |
      | range     | uidd                | 100,200 |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin          | class_name      |
      | [MISSING_PARAM] | Class           |
      | Origin          | [MISSING_PARAM] |
    Then I get an error response of type 400 with error code SVC1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText                    |
      | Missing mandatory parameter:(.*) |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |
      | 0               | 0                  | 0          | 1             | 0                   |

  @request_format
  Scenario Outline: Publication of bindings using unstructured data
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    When I send to $base_api_url/$bindings_url the rule data UNSTRUCTURED_DATA
      | origin  | class_name |
      | Origin0 | Class      |
    Then I get an error response of type 403 with error code POL0011
    And the exceptionText contains <exceptionText_index>
      | exceptionText |
      | (.*)          |

    Examples: 
      | old_class_index | old_instance_index | exceptionText_index |
      | 0               | 0                  | 0                   |

  @request_format
  Scenario Outline: Publication of bindings using malformed data
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    When I send to $base_api_url/$bindings_url the rule data MALFORMED_DATA
      | origin  | class_name |
      | Origin0 | Class      |
    Then I get an error response of type 400 with error code SVC1023
      | api_client_name |
      | Origin0         |
    And the exceptionText contains <exceptionText_index>
      | exceptionText                              |
      | Parser Error: (.*) content not well formed |

    Examples: 
      | old_class_index | old_instance_index | exceptionText_index |
      | 0               | 0                  | 0                   |

  @origin_default
  Scenario Outline: Non valid default value for origin in binding publication
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value   |
      | range     | uidd                | 100,200 |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | DEFAULT | Class      |
      | Default | Class      |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Invalid parameter value:(.*) |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |
      | 0               | 0                  | 0          | 1             | 0                   |

  @origin_default
  Scenario Outline: valid default origin binding publication
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value   |
      | range     | uidd                | 100,200 |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | default | Class      |
    Then I get a success response of type 201 with location <location_index>:
      | location                         |
      | $base_api_url/$bindings_url/(.*) |
    And the response contains the rule data
    And the location returns the rule data

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | location_index |
      | 0               | 0                  | 0          | 0             | 0              |

  @origin_duplicated
  Scenario Outline: Bindings creation for an origin when origin is already created_APIDIRSVR-338
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value   |
      | range     | uidd                | 100,200 |
    And there is a binding already been published with data <old_binding_index>:
      | origin | class_name |
      | Origin | Class |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value   |
      | range     | uidd                | 100,200 |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin | class_name |
      | Origin | Class |
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                                                      |
      | Invalid parameter value: Class-Origin. Supported values are: non-duplicated-origin |

    Examples: 
      | old_class_index | old_instance_index | rule_index | old_binding_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0                 | 0             | 0                   |

  @origin_invalid
  Scenario Outline: Rules publicatione with invalid mandatory data api_client_name
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value   |
      | range     | uidd                | 100,200 |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin                            | class_name |
      | Nón-ASCII                         | Class      |
      | Name.with.symbols                 | Class      |
      | Name with spaces                  | Class      |
      | Non_valid_set1_ºª\\!"·$%&/()=?¿'¡ | Class      |
      | Non_valid_set2_;:,´¨{}[]^`*+_><   | Class      |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Invalid parameter value:(.*) |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |
      | 0               | 0                  | 0          | 1             | 0                   |
      | 0               | 0                  | 0          | 2             | 0                   |
      | 0               | 0                  | 0          | 3             | 0                   |
      | 0               | 0                  | 0          | 4             | 0                   |

  @bindings
  Scenario Outline: Bindings creation with invalid bindings
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And the following bindings in <bindings_index> are available for the context rules:
      | bindings                                            |
      | 123321434324232                                     |
      | ñ                                                   |
      |                                                     |
      | ABC                                                 |
      | a123456789b123456789c123456789d123456789e123456789f |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value   |
      | range     | uidd                | 100,200 |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Invalid parameter value:(.*) |

    Examples: 
      | old_class_index | bindings_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0              | 0          | 0             | 0                   |
      | 0               | 1              | 0          | 0             | 0                   |
      | 0               | 2              | 0          | 0             | 0                   |
      | 0               | 3              | 0          | 0             | 0                   |
      | 0               | 4              | 0          | 0             | 0                   |

  @bindings
  Scenario Outline: Binding creation with non existing bindings
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And the following bindings in <bindings_index> are available for the context rules:
      | bindings                 |
      | 51fc9830fe813b18f4242341 |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value   |
      | range     | uidd                | 100,200 |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                           |
      | Invalid parameter value:(.*). Supported values are:(.*) |

    Examples: 
      | old_class_index | bindings_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0              | 0          | 0             | 0                   |

  @bindings
  @bug
  Scenario Outline: Empty bindings
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And the following bindings in <bindings_index> are available for the context rules:
      | bindings         |
      | [EMPTY_BINDINGS] |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin1 | Class      |
    Then I get an error response of type 400 with error code SVC0002 with location <location_index>:
      | location                         |
      | $base_api_url/$bindings_url/(.*) |

    Examples: 
      | old_class_index | bindings_index | rule_index | binding_index | location_index |
      | 0               | 0              | 0          | 0             | 0              |

  @rule_format
  Scenario Outline: Missing mandatory params in rules
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation       | input_context_param | value           |
      | eq              | missing_value       | [MISSING_PARAM] |
      | eq              | [MISSING_PARAM]     | missing_param   |
      | [MISSING_PARAM] | missing_op          | 1               |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
    Then I get an error response of type 400 with error code SVC1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText                    |
      | Missing mandatory parameter:(.*) |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |
      | 0               | 0                  | 1          | 1             | 0                   |
      | 0               | 0                  | 2          | 2             | 0                   |

  @rule_format
  Scenario Outline: Invalid rules operation
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation  | input_context_param | value |
      | unknown_op | uidd                | 1     |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    Then I get an error response of type 400 with error code SVC0003
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                          |
      | Invalid parameter value:(.*). Possible values are:(.*) |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |

@rule_format
  Scenario Outline: Invalid rules input_parameters
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param               | value |
      | eq        | Uidd                              | 1     |
      | eq        | param with spaces                 | 1     |
      | eq        | param.with.validchar              | 1     |
      | eq        | nón_ascii_param                   | 1     |
      | eq        | españa                            | 1     |
      | eq        | non_valid_set1_ºª\\!"·$%&/()=?¿'¡ | 1     |
      | eq        | non_valid_set2_;:,´¨{}[]^`*+_><   | 1     |
      | eq        |                                   | 1     |
      | eq        | class_name                        | 1     |
      | eq        |   origin                          | 1     |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Invalid parameter value:(.*) |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |
      | 0               | 0                  | 1          | 0             | 0                   |
      | 0               | 0                  | 2          | 0             | 0                   |
      | 0               | 0                  | 3          | 0             | 0                   |
      | 0               | 0                  | 4          | 0             | 0                   |
      | 0               | 0                  | 5          | 0             | 0                   |
      | 0               | 0                  | 6          | 0             | 0                   |
      | 0               | 0                  | 7          | 0             | 0                   |
      | 0               | 0                  | 8          | 0             | 0                   |
      | 0               | 0                  | 9          | 0             | 0                   |

  @rule_format
  Scenario Outline: Valid rules values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value               |
      | eq        | upper_value         | Uidd                |
      | eq        | value_with_spaces   | with spaces         |
      | eq        | value_with_dots     | with.dots           |
      | eq        | non_ascii_value     | España              |
      | eq        | non_valid_set1      | ºª\\!"·$%&/()=?¿'¡  |
      | eq        | non_valid_set2      | ;:´¨{}[]^`*+_><@#// |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
      | Origin4 | Class      |
      | Origin5 | Class      |
    Then I get a success response of type 201 with location <location_index>:
      | location                         |
      | $base_api_url/$bindings_url/(.*) |
    And the response contains the rule data
    And the location returns the rule data

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | location_index |
      | 0               | 0                  | 0          | 0             | 0              |
      | 0               | 0                  | 1          | 1             | 0              |
      | 0               | 0                  | 2          | 2             | 0              |
      | 0               | 0                  | 3          | 3             | 0              |
      | 0               | 0                  | 4          | 4             | 0              |
      | 0               | 0                  | 5          | 5             | 0              |

  @rule_format
  Scenario Outline: Invalid generic rules values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value |
      | eq        | empty_eq            |       |
      | range     | empty_range         | ,     |
      | in        | empty_in            |       |
      | regex     | empty_regex         |       |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Invalid parameter value:(.*) |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |
      | 0               | 0                  | 1          | 0             | 0                   |
      | 0               | 0                  | 2          | 0             | 0                   |
      | 0               | 0                  | 3          | 0             | 0                   |

  @rule_format
  Scenario Outline: Valid rules params and values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param                                                                                                                                           | value                                                                                                                                                                                                          |
      | in        | [STRING_WITH_LENGTH_512] | 1                                                                                                                                                                                                              |
      | in        | long_value                                                                                                                                                    | Long_valueeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee |
      | in        | value_with_spaces                                                                                                                                             | value with spaces                                                                                                                                                                                              |
      | in        | value_no_ascii                                                                                                                                                | España                                                                                                                                                                                                         |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
    Then I get a success response of type 201 with location <location_index>:
      | location                         |
      | $base_api_url/$bindings_url/(.*) |
    And the response contains the rule data
    And the location returns the rule data

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | location_index |
      | 0               | 0                  | 0          | 0             | 0              |
      | 0               | 0                  | 1          | 1             | 0              |
      | 0               | 0                  | 2          | 2             | 0              |
      | 0               | 0                  | 3          | 3             | 0              |

  @rules
  Scenario Outline: Multirules publication for one context_APIDIRSVR-342
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value       |
      | eq        | ob                  | uk          |
      | eq        | ob                  | es          |
      | in        | env                 | pre,pro,int |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin1 | Class      |
    Then I get a success response of type 201 with location <location_index>:
      | location                         |
      | $base_api_url/$bindings_url/(.*) |
    And the response contains the rule data
    And the location returns the rule data

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | location_index |
      | 0               | 0                  | all        | 0             | 0              |

  @happy_path
  Scenario Outline: Addition of an new rule with valid mandatory data_APIDIRSVR-336
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value |
      | eq        | uidd                | 1     |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin                                                                                                              | class_name |
      | Origin                                                                                                              | Class      |
      | [STRING_WITH_LENGTH_512] | Class      |
      | Underscore_name                                                                                                     | Class      |
    Then I get a success response of type 201 with location <location_index>:
      | location                         |
      | $base_api_url/$bindings_url/(.*) |
    And the response contains the rule data
    And the location returns the rule data

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | location_index |
      | 0               | 0                  | 0          | 0             | 0              |
      | 0               | 0                  | 0          | 1             | 0              |
      | 0               | 0                  | 0          | 2             | 0              |
