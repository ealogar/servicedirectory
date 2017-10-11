# -*- coding: utf-8 -*-
Feature: Rule publication
  
  As an operation manager
  I want to define rules associated to a context in order to bind them different instances
  So that I can modified the instances discovery according to my needs

  @eq_rules
  Scenario Outline: Valid Equivalence rules creation_APIDIRSVR-349
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value   |
      | eq        | test                | EsP19ña |
      | eq        | test                | s pace  |
      | eq        | test                | 1       |
      | eq        | test                | 10.5    |
      | eq        | test                | [TRUE]    |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
      | Origin4 | Class      |
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

  @eq_rules
  Scenario Outline: Invalid Equivalence rules creation_APIDIRSVR-350
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value   |
      | eq        | multivalue          | 100,200 |
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

  @in_rules
  Scenario Outline: Valid In rules creation_APIDIRSVR-345
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param  | value      |
      | in        | monovalue_numeric    | 100        |
      | in        | monovalue_string     | test       |
      | in        | multivalue_monotype  | 1,2,3      |
      | in        | multivalue_multitype | [TRUE],[FALSE] |
      | in        | multivalue_multitype | 10.0,-2.5  |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
      | Origin4 | Class      |
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

  @in_rules
  Scenario Outline: Invalid In rules creation_APIDIRSVR-346
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value  |
      | in        | repeated_value      | 1,1,1  |
      | in        | empty_value         | a,,b   |
      | in        | multitype           | 10.5,a |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Invalid parameter value:(.*) |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |
      | 0               | 0                  | 1          | 1             | 0                   |
      | 0               | 0                  | 2          | 2             | 0                   |

  @range_rules
  Scenario Outline: Valid Range rules creation_APIDIRSVR-351
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value                    |
      | range     | uidd                | 100,200                  |
      | range     | uidd                | a,b                      |
      | range     | uidd                | 10.50,10.60              |
      | range     | uidd                | -1,1                     |
      | range     | uidd                | -200,-100                |
      | range     | max_int             | -21474836490,21474836490 |
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

  @range_rules
  Scenario Outline: Invalid Range rules creation_APIDIRSVR-352
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value       |
      | range     | repeated            | 100,100     |
      | range     | not_a_range         | 100,200,300 |
      | range     | inverted_range      | 200,100     |
      | range     | not_a_range         | 100         |
      | range     | multi_value         | a,200       |
      | range     | boolean_range       | [TRUE],[FALSE]  |
      | range     | empty_rang          | 1,          |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
      | Origin4 | Class      |
      | Origin5 | Class      |
      | Origin6 | Class      |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Invalid parameter value:(.*) |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |
      | 0               | 0                  | 1          | 1             | 0                   |
      | 0               | 0                  | 2          | 2             | 0                   |
      | 0               | 0                  | 3          | 3             | 0                   |
      | 0               | 0                  | 4          | 4             | 0                   |
      | 0               | 0                  | 5          | 5             | 0                   |
      | 0               | 0                  | 6          | 6             | 0                   |

  @regex_rules
  Scenario Outline: Valid Regex rules creation_APIDIRSVR-347
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value            |
      | regex     | simple_regex        | (.*)             |
      | regex     | complex_regex       | /^#?([a-f0-9]{6}) |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
    Then I get a success response of type 201 with location <location_index>:
      | location                         |
      | $base_api_url/$bindings_url/(.*) |
    And the response contains the rule data
    And the location returns the rule data

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | location_index |
      | 0               | 0                  | 0          | 0             | 0              |
      | 0               | 0                  | 1          | 1             | 0              |

  @regex_rules
  Scenario Outline: Invalid Regex rules creation_APIDIRSVR-348
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value               |
      | regex     | multivalue          | .*,/^#?([a-f0-9]{6} |
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
