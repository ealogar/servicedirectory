# -*- coding: utf-8 -*-
Feature: Instance Discovering
  
  As a class consumer
  I would like the Service Directory to give me the most suitable instance for me, routing the request based on the attributes defining the instance.
  So that I can consume the class

  @done
  Scenario Outline: Discovery with: No client_name, Valid search params and a default rule matching defined with bindings
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | regex     | version             | (.*)  |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | default | Class        |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | version | class_name |
      | v2.0    | Class        |
    Then I get a success response of type 200 with a result set of size 1
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                    | environment |
      | Class        | v2.0    | http://instance.tid.es | production  |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | instance_index |
      | 0             | 0                  | 0               | 0             | 0            | 0              |

  @done
  Scenario Outline: Discovery with: No client_name and invalid search params (Non existing params)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v2.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | regex     | other_context_param | (.*)  |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | default | Class        |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | wrong_param        | class_name |
      | non_existing_param | Class        |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                               |
      | Resource binding-Class-default does not exist |

    Examples: 
      | old_class_index | old_instance_index | params_index | exceptionText_index | context_index |operation_index|
      | 0             | 0                  | 0            | 0                   | 0             |0|

  @done
  Scenario Outline: Discovery with: No client_name and invalid search params (Params of other context)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                            | environment |
      | v2.0    | http://instance_client0.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | eq        | other_context_param | 1     |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | Client0 | Class        |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                            | environment |
      | v2.0    | http://instance_default.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param   | value |
      | eq        | default_context_param | 1     |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | default | Class        |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | other_context_param | class_name |
      | 1                   | Class        |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                               |
      | Resource binding-Class-default does not exist |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | exceptionText_index |
      | 0             | 0                  | 0               | 0             | 0            | 0                   |

  @done
  Scenario Outline: Discovery with: No client_name and inalid search params (empty_params)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v2.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                        | environment |
      | v2.0    | http://instance_old.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | regex     | test                | (.*)  |
      | eq        | test                | 1     |
      | in        | test                | 1,2   |
      | range     | test                | 1,10  |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | default | Class        |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | test | class_name |
      |      | Class        |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                 |
      | Invalid parameter value: (.*) |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | instance_index | instance_order_index | exceptionText_index |
      | 0             | 0                  | 0               | 0             | 0            | 0              | 0                    | 0                   |
      | 0             | 0                  | 1               | 0             | 0            | 0              | 0                    | 0                   |
      | 0             | 0                  | 2               | 0             | 0            | 0              | 0                    | 0                   |
      | 0             | 0                  | 3               | 0             | 0            | 0              | 0                    | 0                   |

  @done
  Scenario Outline: Discovery with: No client_name, Valid search params, a single default rule matching defined with bindings and deleted bindings
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v2.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | regex     | version             | (.*)  |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | default | Class        |
    And the instance published in position <instance_order_index> has been deleted
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | version | class_name |
      | v1.0    | Class        |
    Then I get an error response of type 404 with error code SVC2003
    And the exceptionText contains <exceptionText_index>
      | exceptionText                  |
      | Resource (.*) has been deleted |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | instance_order_index | exceptionText_index |
      | 0             | 0                  | 0               | 0             | 0            | 0                    | 0                   |

  @done_revised
  Scenario Outline: Discovery with: No client_name, Valid search params, multiples default rule matching defined with bindings and deleted bindings
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v2.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                        | environment |
      | v2.0    | http://instance_old.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | regex     | version             | (.*)  |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                        | environment |
      | v2.0    | http://instance_new.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | regex     | version             | (.*)  |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | default | Class        |
    And the instance published in position <instance_order_index> has been deleted
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | version | class_name |
      | v1.0    | Class        |
    Then I get an error response of type 404 with error code SVC2003
    And the exceptionText contains <exceptionText_index>
      | exceptionText                  |
      | Resource (.*) has been deleted |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | instance_index | instance_order_index | exceptionText_index |
      | 0             | 0                  | 0               | 0             | 0            | 0              | 0                    | 0                   |

  @done_revised
  Scenario Outline: Discovery with: No client_name, Valid search params, single default rule matching defined with empty bindings
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v2.0             |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | regex     | version             | (.*)  |
    And the following bindings in <bindings_index> are available for the context rules:
      | bindings         |
      | [EMPTY_BINDINGS] |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | default | Class        |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | version | class_name |
      | v2.0    | Class        |
    Then I get an error response of type 404 with error code SVC2002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                               |
      | Binding resource Class-default does not exist |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | bindings_index | exceptionText_index |
      | 0             | 0                  | 0               | 0             | 0            | 0              | 0                   |

  @done_revised
  Scenario Outline: Discovery with:  No client_name, Valid search params and non matching default rules
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v2.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | eq        | version             | v2.0   |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | default | Class        |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | version | class_name |
      | v1.0    | Class        |
    Then I get an error response of type 404 with error code SVC2002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                               |
      | Resource binding-Class-default does not exist |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | exceptionText_index |
      | 0             | 0                  | 0               | 0             | 0            | 0                   |

  @done_revised
  Scenario Outline: Discovery with:  No client_name, Valid search params and no default rules
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v2.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | regex     | version             | (.*)  |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | Client0 | Class        |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | version | class_name |
      | v2.0    | Class        |
    Then I get an error response of type 404 with error code SVC2002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                        |
      | Binding resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | exceptionText_index |
      | 0             | 0                  | 0               | 0             | 0            | 0                   |

  @done_revised
  Scenario Outline: Discovery with: Wrong client_name context
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v2.0             |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin              | class_name |
      | Non_existing_client | Class        |
    Then I get an error response of type 404 with error code SVC2002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                        |
      | Binding resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | exceptionText_index |
      | 0             | 0                  | 0            | 0              | 0                   |

  @done_revised
  Scenario Outline: Discovery without: missign params
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v2.0             |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin |
      | origin |
    Then I get an error response of type 400 with error code SVC1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText                    |
      | Missing mandatory parameter:(.*) |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | exceptionText_index |
      | 0             | 0                  | 0            | 0              | 0                   |

  @done_revised
  Scenario Outline: Discovery of an unexisting class_TDAFBA-689
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has not already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | version | class_name         |
      | v1.0    | Non_existing_class |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                              |
      | Resource Non_existing_class does not exist |

    Examples: 
      | old_class_index | old_instance_index | params_index | exceptionText_index |
      | 0             | 0                  | 0            | 0                   |

  @db_revised
  Scenario Outline: Discovery when the DB is down_TDAFBA-448
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | test_param |
      | v1.0    | http://instance.tid.es | test_value |
    And the DB has stopped working
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | version |
      | v1.0    |
    Then I get an error response of type 500 with error code SVR1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText                        |
      | Generic Server Error: internal error |

    Examples: 
      | old_class_index | old_instance_index | params_index | exceptionText_index |
      | 0             | 0                  | 0            | 0                   |

  @multirules_revised
  Scenario Outline: Discovery with: client_name, Valid search params and multi rule matching defined with bindings
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | range     | param_1             | 1,5   |
      | eq        | param_2             | 2     |
      | regex     | param_3             | (.*)  |
      | in        | param_4             | a,b   |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | Client0 | Class        |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin  | param_1 | param_2 | param_3   | param_4 | class_name |
      | Client0 | 3       | 2       | any_value | a       | Class        |
    Then I get a success response of type 200
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                    | environment |
      | Class        | v2.0    | http://instance.tid.es | production  |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | instance_index |
      | 0             | 0                  | all             | 0             | 0            | 0              |

  @multirules_revised
  Scenario Outline: Discovery with: client_name, Valid search params and multi rule not matching defined with bindings
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | range     | param_1             | 1,5   |
      | eq        | param_2             | 2     |
      | in        | param_3             | a,b   |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | Client0 | Class        |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin  | param_1 | param_2 | param_3 | class_name |
      | Client0 | 3       | 2       | c       | Class        |
      | Client0 | 6       | 3       | c       | Class        |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                               |
      | Resource binding-Class-Client0 does not exist |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | instance_index | exceptionText_index |
      | 0             | 0                  | all             | 0             | 0            | 0              | 0                   |
      | 0             | 0                  | all             | 0             | 1            | 0              | 0                   |

  @multirules_revised
  Scenario Outline: Discovery with: client_name, Valid search params and multi rule and conflictive values in first rule
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value   |
      | in        | param_1             | 1,5     |
      | in        | param_1             | 1.0,5.0 |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | Client0 | Class        |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin  | param_1 | class_name |
      | Client0 | v1.0     | Class        |
      | Client0 | 5.0     | Class        |
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                             |
      | Invalid parameter value: (.*). Supported values are: (.*) |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | instance_index | exceptionText_index |
      | 0             | 0                  | all             | 0             | 0            | 0              | 0                   |
      | 0             | 0                  | all             | 0             | 1            | 0              | 0                   |

  @multigroups_revised
  Scenario Outline: Discovery with: client_name, Valid search params and multi groups all matching defined with bindings
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class0       | Class  | v1.0             |
      | Class1       | Class  | v1.0             |
      | Class2       | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                           | environment |
      | v2.0    | http://instance_group1.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | range     | param_1             | 1,5   |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                           | environment |
      | v3.0    | http://instance_group2.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | range     | param_1             | 1,10  |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                           | environment |
      | v4.0    | http://instance_group3.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | eq        | param_1             | 9     |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | Client0 | Class0       |
      | Client0 | Class1       |
      | Client0 | Class2       |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin  | param_1 | class_name |
      | Client0 | 1       | Class0       |
      | Client0 | 6       | Class1       |
      | Client0 | 9       | Class2       |
    Then I get a success response of type 200
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                           | environment |
      | Class0       | v2.0    | http://instance_group1.tid.es | production  |
      | Class1       | v3.0    | http://instance_group2.tid.es | production  |
      | Class2       | v3.0    | http://instance_group2.tid.es | production  |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | instance_index |
      | 0             | 0                  | 0               | 0             | 0            | 0              |
      | 1             | 0                  | 0               | 1             | 1            | 1              |
      | 2             | 0                  | 0               | 2             | 2            | 2              |

  @simple_context_jump
  Scenario Outline: Discovery with: client_name, default, Valid search params and a matching rule defined with bindings ( Origin not existing)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                            | environment |
      | v2.0    | http://instance_client0.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | eq        | param_1             | 1     |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | Client0 | Class        |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                            | environment |
      | v2.0    | http://instance_default.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | eq        | param_1             | 2     |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | default | Class        |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin  | param_1 | class_name |
      | Client1 | 2       | Class        |
    Then I get an error response of type 404 with error code SVC2002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                        |
      | Binding resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | instance_index | exceptionText_index |
      | 0             | 0                  | 0               | 0             | 0            | 0              | 0                   |

  @simple_context_jump_revised
  Scenario Outline: Discovery with: client_name, default, Valid search params and a matching rule defined with bindings ( Origin not included)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                            | environment |
      | v2.0    | http://instance_client0.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | eq        | param_1             | 1     |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | Client0 | Class        |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                            | environment |
      | v2.0    | http://instance_default.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | eq        | param_1             | 2     |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | default | Class        |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | param_1 | class_name |
      | 2       | Class        |
    Then I get a success response of type 200
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                            | environment |
      | Class        | v2.0    | http://instance_default.tid.es | production  |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | instance_index |
      | 0             | 0                  | 0               | 0             | 0            | 0              |

  @complex_context_jump_revised
  Scenario Outline: Discovery with: client_name, Valid search params and multi groups all matching defined with bindings
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class0       | Class  | v1.0             |
      | Class1       | Class  | v1.0             |
      | Class2       | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                         | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance_loc1.tid.es | production  | filter          | filter_value      |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | range     | param_1             | 1,5   |
      | eq        | param_2             | 5     |
      | in        | param_3             | a,b   |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v3.0    | http://instance.tid.es | production  | filter          | filter_value      |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value   |
      | range     | param_4             | 5,10    |
      | eq        | param_2             | 8       |
      | in        | param_3             | a,b,c,d |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | Client0 | Class0       |
      | Client0 | Class1       |
      | Client0 | Class2       |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                            | environment |
      | v2.0    | http://instance_default.tid.es | production  |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | regex     | param_5             | (.*)  |
    And the previous bindings are published for the context <context_index>:
      | origin  | class_name |
      | default | Class0       |
      | default | Class1       |
      | default | Class2       |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin  | param_1         | param_2 | param_3 | param_4         | class_name |
      | Client0 | 2               | 5       | a       | [MISSING_PARAM] | Class0       |
      | Client0 | [MISSING_PARAM] | 8       | a       | 8               | Class1       |
      | Client0 | 1               | 8       | a       | 8               | Class2       |
    Then I get a success response of type 200
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                         | environment | attributes_keys | attributes_values |
      | Class0       | v2.0    | http://instance_loc1.tid.es | production  | filter          | filter_value      |
      | Class1       | v3.0    | http://instance.tid.es      | production  | filter          | filter_value      |
      | Class2       | v3.0    | http://instance.tid.es      | production  | filter          | filter_value      |

    Examples: 
      | old_class_index | old_instance_index | operation_index | context_index | params_index | instance_index |
      | 0             | 0                  | all             | 0             | 0            | 0              |
      | 1             | 0                  | all             | 1             | 1            | 1              |
      | 2             | 0                  | all             | 2             | 2            | 2              |
