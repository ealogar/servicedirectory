# -*- coding: utf-8 -*-
Feature: CLI Binding Management
  
    As an operation manager
    I want to create, query and delete service bindings
    So that I can deliver the desired instance to a client request

  @happy_path @create_binding
  Scenario Outline: Create an binding with mandatory params and existing bindings file
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the binding:
      | id                       | class_name | origin      | binding_rules |
      | 5253d9a3fe813b07289be43c | test       | test_origin | {}            |
    When I request the operation <operation_index>:
      | options | operation       | arguments                                                                |
      |         | bindings create | test test_origin  ./component/cli/cli_bindings_management/mock_file.json |
    Then the result set contains the data <data_index>:
      | operation_type   | operator                                   | message |
      | Created bindings | for class "test" and origin "test_origin": | [EMPTY] |

    Examples: 
      | cliconfig_index | data_index | operation_index | body_index |
      | 0               | 0          | 0               | 0          |

  @missing_file @create_binding
  Scenario Outline: Create an binding with mandatory params and non existing bindings file
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the binding:
      | id                       | class_name | origin      | binding_rules |
      | 5253d9a3fe813b07289be43c | test       | test_origin | {}            |
    When I request the operation <operation_index>:
      | options | operation       | arguments                                |
      |         | bindings create | test test_origin  non_existing_file.json |
    Then the error contains the data <error_index>:
      | error_type   | message                                  |
      | [CLI Error]: | Not existing file non_existing_file.json |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |
      
 
  @empty_file @create_binding
  Scenario Outline: Create an binding with mandatory params and empty file
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the binding:
      | id                       | class_name | origin      | binding_rules |
      | 5253d9a3fe813b07289be43c | test       | test_origin | {}            |
    When I request the operation <operation_index>:
      | options | operation       | arguments                                |
      |         | bindings create | test test_origin  ./component/cli/cli_bindings_management/empty_file.json |
    Then the error contains the data <error_index>:
      | error_type   | message                                  |
      | [CLI Error]: | Error parsing JSON file: No JSON object could be decoded |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |
      
   
  @bad_format @create_binding
  Scenario Outline: Create an binding with mandatory params and file with bad format
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the binding:
      | id                       | class_name | origin      | binding_rules |
      | 5253d9a3fe813b07289be43c | test       | test_origin | {}            |
    When I request the operation <operation_index>:
      | options | operation       | arguments                                |
      |         | bindings create | test test_origin  ./component/cli/cli_bindings_management/bad_file.json |
    Then the error contains the data <error_index>:
      | error_type   | message                                  |
      | [CLI Error]: | Error parsing JSON file: No JSON object could be decoded |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |
      
  @happy_path @create_binding
  Scenario Outline: Create an binding with mandatory params and existing bindings file with non ASCII chars
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the binding:
      | id                       | class_name | origin      | binding_rules |
      | 5253d9a3fe813b07289be43c | test       | test_origin | {}            |
    When I request the operation <operation_index>:
      | options | operation       | arguments                                                                |
      |         | bindings create | test test_origin  ./component/cli/cli_bindings_management/non_ascii_file.json |
    Then the result set contains the data <data_index>:
      | operation_type   | operator                                   | message |
      | Created bindings | for class "test" and origin "test_origin": | [EMPTY] |

    Examples: 
      | cliconfig_index | data_index | operation_index | body_index |
      | 0               | 0          | 0               | 0          |
 
 
