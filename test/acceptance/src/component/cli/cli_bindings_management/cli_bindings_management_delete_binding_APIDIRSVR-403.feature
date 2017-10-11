# -*- coding: utf-8 -*-
Feature: CLI Binding Management
  
    As an operation manager
    I want to create, query and delete service bindings
    So that I can deliver the desired instance to a client request

  @happy_path @delete_binding
  Scenario Outline: Delete a binding
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the binding when is searched:
      | id                       | class_name | origin      | binding_rules                                                                                                                           |
      | 5253d9a3fe813b07289be43c | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e18"], "group_rules": [{"operation": "eq", "input_context_param": "origin", "value": ["testa"]}]}] |
    And the SD is ready to accept the deletion of resource <sd_config_index>:
      | resource                                |
      | sd/v1/bindings/5253d9a3fe813b07289be43c |
    When I request the operation <operation_index>:
      | options | operation       | arguments        |
      |         | bindings delete | test test_origin |
    Then the result set contains the data <data_index>:
      | operation_type              | operator                     | message |
      | Deleted bindings for class: | test and origin: test_origin | [EMPTY] |

    Examples: 
      | sd_config_index | operation_index | data_index |
      | 0               | 0               | 0          |

  @missing_resource @delete_binding
  Scenario Outline: Delete a binding when the binding origin-class_name does not exists
    Given the CLI is installed and ready to be executed
    And the SD is ready to return an error 404 for binding discovery:
      | exceptionId | exceptionText                            |
      | SVC1006     | Resource test-test_origin does not exist |
    When I request the operation <operation_index>:
      | options | operation       | arguments        |
      |         | bindings delete | test test_origin |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText                            |
      | [SD Error]: | SVC1006     | Resource test-test_origin does not exist |

    Examples: 
      | sd_config_index | operation_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |

  @missing_resource @delete_binding
  Scenario Outline: Delete a binding when the id recovered does not existis
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the binding when is searched:
      | id                       | class_name | origin      | binding_rules                                                                                                                           |
      | 5253d9a3fe813b07289be43c | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e18"], "group_rules": [{"operation": "eq", "input_context_param": "origin", "value": ["testa"]}]}] |
    And the SD is ready to return an error 404 for binding deletion of binding 5253d9a3fe813b07289be43c:
      | exceptionId | exceptionText                            |
      | SVC1006     | Resource test-test_origin does not exist |
    When I request the operation <operation_index>:
      | options | operation       | arguments        |
      |         | bindings delete | test test_origin |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText                            |
      | [SD Error]: | SVC1006     | Resource test-test_origin does not exist |

    Examples: 
      | sd_config_index | operation_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |

  @missing_resource @delete_binding
  Scenario Outline: Delete a binding when and the id can not be recovered from binding query
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the binding when is searched:
      | class_name | origin      | binding_rules                                                                                                                           |
      | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e18"], "group_rules": [{"operation": "eq", "input_context_param": "origin", "value": ["testa"]}]}] |
    And the SD is ready to accept the deletion of resource <sd_config_index>:
      | resource                                             |
      | sd/v1/classes/test/bindings/5253d9a3fe813b07289be43c |
    When I request the operation <operation_index>:
      | options | operation       | arguments        |
      |         | bindings delete | test test_origin |
    Then the error contains the data <error_index>:
      | error_type   | message                                                                          |
      | [CLI Error]: | It seems that something goes wrong. Contact the operator for further assistance. |

    Examples: 
      | sd_config_index | operation_index | error_index |
      | 0               | 0               | 0           |

  @missing_params @delete_instance
  Scenario Outline: Delete an instance with missing or extra params
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation       | arguments |
      |         | bindings delete |           |
      |         | bindings delete | test      |
    Then the result set contains the help info

    Examples: 
      | operation_index |
      | 0               |
      | 1               |
