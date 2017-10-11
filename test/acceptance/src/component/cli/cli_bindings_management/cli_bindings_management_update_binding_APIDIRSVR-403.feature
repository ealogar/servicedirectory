# -*- coding: utf-8 -*-
Feature: CLI Endpoint Management
  
    As an operation manager
    I want to create, query and delete service instance
    So that I can modify the list of service endpoints available to Service Directory clients

  @happy_path @update_binding
  Scenario Outline: Update an existing binding
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the following bindings:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    And the SD is ready to return the updated binding 5253d9a3fe813b07289be431:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    When I request the operation <operation_index>:
      | options | operation       | arguments                                                                |
      |         | bindings update | test test_origin  ./component/cli/cli_bindings_management/mock_file.json |
    Then the result set contains the data <data_index>:
      | operation_type  | operator                                | message |
      | Updated binding | for class: test and origin: test_origin | [EMPTY] |

    Examples: 
      | operation_index | sd_config_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |

  @missing_file @update_binding
  Scenario Outline: Update a binding with mandatory params and non existing bindings file
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the following bindings:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    And tthe SD is ready to return the updated binding 5253d9a3fe813b07289be431:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    When I request the operation <operation_index>:
      | options | operation       | arguments                                |
      |         | bindings update | test test_origin  non_existing_file.json |
    Then the error contains the data <error_index>:
      | error_type   | message                                  |
      | [CLI Error]: | Not existing file non_existing_file.json |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @empty_file @update_binding
  Scenario Outline: Update a binding with mandatory params and empty file
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the following bindings:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    And tthe SD is ready to return the updated binding 5253d9a3fe813b07289be431:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    When I request the operation <operation_index>:
      | options | operation       | arguments                                                                 |
      |         | bindings update | test test_origin  ./component/cli/cli_bindings_management/empty_file.json |
    Then the error contains the data <error_index>:
      | error_type   | message                                                  |
      | [CLI Error]: | Error parsing JSON file: No JSON object could be decoded |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @bad_format @update_binding
  Scenario Outline: Update a binding with mandatory params and file with bad format
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the following bindings:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    And tthe SD is ready to return the updated binding 5253d9a3fe813b07289be431:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    When I request the operation <operation_index>:
      | options | operation       | arguments                                                               |
      |         | bindings update | test test_origin  ./component/cli/cli_bindings_management/bad_file.json |
    Then the error contains the data <error_index>:
      | error_type   | message                                                  |
      | [CLI Error]: | Error parsing JSON file: No JSON object could be decoded |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @happy_path @update_binding
  Scenario Outline: Update a binding with mandatory params and existing bindings file with non ASCII chars
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the following bindings:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    And tthe SD is ready to return the updated binding 5253d9a3fe813b07289be431:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    When I request the operation <operation_index>:
      | options | operation       | arguments                                                                     |
      |         | bindings update | test test_origin  ./component/cli/cli_bindings_management/non_ascii_file.json |
    Then the result set contains the data <data_index>:
      | operation_type  | operator                                | message |
      | Updated binding | for class: test and origin: test_origin | [EMPTY] |

    Examples: 
      | cliconfig_index | data_index | operation_index | body_index |
      | 0               | 0          | 0               | 0          |

  @missing_param @update_binding
  Scenario Outline: Update an existing binding with missing attributes
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the following bindings:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    And tthe SD is ready to return the updated binding 5253d9a3fe813b07289be431:
      | id                       | class_name | origin      | binding_rules                                                   |
      | 5253d9a3fe813b07289be431 | test       | test_origin | [{"bindings": ["5257b764fe813b191cee1e17"], "group_rules": []}] |
    When I request the operation <operation_index>:
      | options | operation      | arguments        |
      |         | binding update |                  |
      |         | binding update | test             |
      |         | binding update | test test_origin |
    Then the result set contains the help info

    Examples: 
      | operation_index | sd_config_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |
      | 1               | 0               | 0          | 0           |
      | 2               | 0               | 0          | 0           |
