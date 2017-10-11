# -*- coding: utf-8 -*-
Feature: Rule publication
  
  As a operation manager
  I want to filter the list of bindings
  So that I can find a specific binding in the list

  @happy_path
  Scenario: Obtaining results over an empty bindigns list with out params
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I request the resource $base_api_url/$bindings_url
    Then I get a success response of type 200 with a result set of size 0

  @happy_path
  Scenario Outline: Obtaining results over an empty bindigns list with params
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I request the resource $base_api_url/$bindings_url with parameters <params_index>:
      | origin  | class_name |
      | Origin3 | Class2     |
    Then I get a success response of type 200 with a result set of size 0

    Examples: 
      | params_index |
      | 0            |

  @happy_path
  Scenario Outline: Get the list of bindings
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class1     | New Class   | v1.0            |
   And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <old_rule_index>:
      | operation | input_context_param | value |
      | eq        | uidd                | 1     |
    And the previous bindings are published for the context <old_binding_index>:
      | origin  | class_name |
      | Origin1 | Class1     |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class2     | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <old_rule_index>:
      | operation | input_context_param | value |
      | eq        | uidd                | 2     |
    And the previous bindings are published for the context <old_binding_index>:
      | origin  | class_name |
      | Origin2 | Class2     |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class3     | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <old_rule_index>:
      | operation | input_context_param | value |
      | eq        | uidd                | 3     |
    And the previous bindings are published for the context <old_binding_index>:
      | origin  | class_name |
      | default | Class3     |
    When I request the resource $base_api_url/$bindings_url
    Then I get a success response of type 200 with a result set of size 3
    And the result set contains the binding <binding_index>:
      | origin  | class_name |
      | Origin1 | Class1     |
    And the result set contains the binding <binding_index>:
      | origin  | class_name |
      | Origin2 | Class2     |
    And the result set contains the binding <binding_index>:
      | origin  | class_name |
      | default | Class3     |

    Examples: 
      | old_class_index | old_instance_index | old_rule_index | old_binding_index | params_index | rule_index | binding_index |
      | 0               | 0                  | 0              | 0                 | 0            | 0          | 0             |
