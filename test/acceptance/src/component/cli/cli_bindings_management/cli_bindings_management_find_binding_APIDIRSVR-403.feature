# -*- coding: utf-8 -*-
Feature: CLI Endpoint Management
  
    As an operation manager
    I want to create, query and delete service instance
    So that I can modify the list of service endpoints available to Service Directory clients

  @happy_path @get_binding
  Scenario Outline: Find all the bindings with valid params
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the following bindings:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    When I request the operation <operation_index>:
      | options | operation    | arguments        |
      |         | bindings get | test test_origin |
    Then the result set contains the item <item_index>:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |

    Examples: 
      | operation_index | item_index |
      | 0               | 0          |

  @missing_params @get_binding
  Scenario Outline: Get a binding with extra or missing params
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation    | arguments              |
      |         | bindings get | test test_origin extra |
      |         | bindings get |                        |
      |         | bindings get | test                   |
    Then the result set contains the help info

    Examples: 
      | operation_index |
      | 0               |
      | 1               |
      | 2               |

  @happy_path @find_bindings
  Scenario Outline: Find all the bindings with valid params
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the following bindings:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
      | 5253d9a3fe813b07289be432 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e18"], "group_rules": []}] |
      | 5253d9a3fe813b07289be433 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e19"], "group_rules": []}] |
    When I request the operation <operation_index>:
      | options | operation     | arguments                           |
      |         | bindings find |                                     |
      |         | bindings find | class_name=test                     |
      |         | bindings find | origin=test_origin                  |
      |         | bindings find | class_name=test  origin=test_origin |
    Then the result set contains:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
      | 5253d9a3fe813b07289be432 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e18"], "group_rules": []}] |
      | 5253d9a3fe813b07289be433 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e19"], "group_rules": []}] |

    Examples: 
      | operation_index |
      | 0               |
      | 1               |
      | 2               |
      | 3               |

  @bad_param @find_bindings
  Scenario Outline: Find all the bindings with invalid params format
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation     | arguments       |
      |         | bindings find | class_name test |
      |         | bindings find | other=test      |
    Then the error contains the data <error_index>:
      | error_type   | message                                        |
      | [CLI Error]: | <params> should match the format <key>=<value> |
      | [CLI Error]: | "other" cannot be part of <params>             |

    Examples: 
      | operation_index | error_index |
      | 0               | 0           |
      | 1               | 1           |

  @wrong_param @find_bindings
  Scenario Outline: Find bindings with repeated params
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation     | arguments                             |
      |         | bindings find | origin=test_origin origin=test_origin |
    Then the error contains the data <error_index>:
      | error_type   | message                          |
      | [CLI Error]: | origin <key> can not be repeated |

    Examples: 
      | operation_index | error_index |
      | 0               | 0           |

  @happy_path @find_bindings
  Scenario Outline: Find bindings with no results
    Given the CLI is installed and ready to be executed
    And the SD is ready to return no bindings
    When I request the operation <operation_index>:
      | options | operation     | arguments                             |
      |         | bindings find | class_name=no_class  origin=no_origin |
    Then the result set contains the data <data_index>:
      | operation_type | operator | message                                    |
      | [EMPTY]        | [EMPTY]  | No bindings matching these filter criteria |

    Examples: 
      | data_index | operation_index |
      | 0          | 0               |

  @not_expected_response @find_binding
  Scenario Outline: Find binding with an unexpected response ( Single response instead and array)
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the binding:
      | id                       | class_name | origin      | binding_rules |
      | 5253d9a3fe813b07289be43c | test       | test_origin | {}            |
    When I request the operation <operation_index>:
      | options | operation    | arguments        |
      |         | bindings get | test test_origin |
    Then the error contains the data <error_index>:
      | error_type   | message                                                                          |
      | [CLI Error]: | It seems that something goes wrong. Contact the operator for further assistance. |

    Examples: 
      | sd_config_index | operation_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |
