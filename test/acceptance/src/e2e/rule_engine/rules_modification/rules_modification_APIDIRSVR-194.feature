# -*- coding: utf-8 -*-
Feature: Rule modification
  
  As an operation manager
  I want to modify rules associated to an origin in order to update them
  So that I can modified the instances discovery according to my needs on the fly


  @rule_format
  Scenario Outline: Binding update to valid rules params and values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <old_rule_index>:
      | operation | input_context_param | value   |
      | range     | uidd                | 100,200 |
    And the previous bindings are pusblished for the context <old_binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param                                                                                                                                           | value                                                                                                                                                                                                          |
      | in        | [STRING_WITH_LENGTH_512] | 1                                                                                                                                                                                                              |
      | in        | long_value                                                                                                                                                    | Long_valueeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee |
      | in        | value_with_spaces                                                                                                                                             | value with spaces                                                                                                                                                                                              |
      | in        | value_no_ascii                                                                                                                                                | España                                                                                                                                                                                                         |
    When I put in $base_api_url/$bindings_url/$binding_id the binding data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
    Then I get a success response of type 200 with the updated binding data
    And the URL $base_api_url/$bindings_url/$binding_id returns the updated binding data

    Examples: 
      | old_class_index | old_instance_index | old_rule_index | old_binding_index | rule_index | binding_index | location_index |
      | 0               | 0                  | 0              | 0                 | 0          | 0             | 0              |
      | 0               | 0                  | 0              | 1                 | 1          | 1             | 0              |
      | 0               | 0                  | 0              | 2                 | 2          | 2             | 0              |
      | 0               | 0                  | 0              | 3                 | 3          | 3             | 0              |

  @rules
  Scenario Outline: Binding update to multirules
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <old_rule_index>:
      | operation | input_context_param | value   |
      | range     | uidd                | 100,200 |
    And the previous bindings are pusblished for the context <old_binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value       |
      | eq        | ob                  | uk          |
      | eq        | ob                  | es          |
      | in        | env                 | pre,pro,int |
    When I put in $base_api_url/$bindings_url/$binding_id the binding data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    Then I get a success response of type 200 with the updated binding data
    And the URL $base_api_url/$bindings_url/$binding_id returns the updated binding data

    Examples: 
      | old_class_index | old_instance_index | old_rule_index | old_binding_index | rule_index | binding_index |
      | 0               | 0                  | 0              | 0                 | all        | 0             |

  @rules
  Scenario Outline: Binding update to monorule
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
    And the previous bindings are pusblished for the context <old_binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <old_rule_index>:
      | operation | input_context_param | value   |
      | range     | uidd                | 100,200 |
    When I put in $base_api_url/$bindings_url/$binding_id the binding data <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    Then I get a success response of type 200 with the updated binding data
    And the URL $base_api_url/$bindings_url/$binding_id returns the updated binding data

    Examples: 
      | old_class_index | old_instance_index | old_rule_index | old_binding_index | rule_index | binding_index |
      | 0               | 0                  | all            | 0                 | 0          | 0             |
