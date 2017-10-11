# -*- coding: utf-8 -*-
Feature: Rule deletion
  
  As a operation manager I would like to delete a context and its rules so that the rules becomes unavailable.

  Scenario Outline: Deletion of an context when the DB is down
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
    And the previous bindings are pusblished for the context <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    And the DB has stopped working
    When I delete $base_api_url/$bindings_url/$binding_id
    Then I get an error response of type 500 with error code SVR1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText            |
      | Generic Server Error(.*) |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |

  @happy_path
  Scenario Outline: Deletion of a binding with a single rule
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
      | eq        | rule                | 1     |
    And the previous bindings are pusblished for the context <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    When I delete $base_api_url/$bindings_url/$binding_id
    Then I get a success response of type 204
    And the URL $base_api_url/$bindings_url/$binding_id returns the error code 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |

  Scenario Outline: Deletion of a non_existing binding with a single rule
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
    And the previous bindings are pusblished for the context <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    When I delete $base_api_url/$bindings_url/112345e345g4555g
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |

  Scenario Outline: Deletion of a binding with a multiples rules
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
    And the previous bindings are pusblished for the context <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    When I delete $base_api_url/$bindings_url/$binding_id
    Then I get a success response of type 204
    And the URL $base_api_url/$bindings_url/$binding_id returns the error code 404 with error code SVC1006

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index |
      | 0               | 0                  | all        | 0             |

  Scenario Outline: Deletion of a binding without specifying binding_rules path
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
    And the previous bindings are pusblished for the context <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
    When I delete $base_api_url/$bindings_url
    Then I get an error response of type 405 with error code SVC1003
    And the exceptionText contains <exceptionText_index>
      | exceptionText                           |
      | Requested Operation does not exist:(.*) |

    Examples: 
      | old_class_index | old_instance_index | rule_index | binding_index | exceptionText_index |
      | 0               | 0                  | 0          | 0             | 0                   |
