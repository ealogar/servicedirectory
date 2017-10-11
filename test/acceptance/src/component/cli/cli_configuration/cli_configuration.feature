# -*- coding: utf-8 -*-
Feature: CLI Endpoint Management
  
    As an operation manager
    I want to configure the CLI client
    So that I can use the service directory with the desired configuration

  @file_problem
  Scenario Outline: Use SD when the config file is missing. Request performed
    Given the CLI is installed and ready to be executed
    And the CLI config file has been removed
    When I request the operation <operation_index>:
      | operation | arguments |
      | info      |           |
    Then the error contains the data <error_index>:
      | error_type   | message                 |
      | [CLI Error]: | Error reading file (.*) |

    Examples: 
      | cliconfig_index | error_index | operation_index |
      | 0               | 0           | 0               |

  @file_problem
  Scenario Outline: Use SD when the config file is missing. Configuration shown
    Given the CLI is installed and ready to be executed
    And the CLI config file has been removed
    When I request the operation <operation_index>:
      | operation | arguments |
      |           | -s        |
    Then the error contains the data <error_index>:
      | message                                                  |
      | Path to default config: (.*)                             |
      | Content of file:                                         |
      | Default config file not found. It must have been deleted |

    Examples: 
      | operation_index | error_index |
      | 0               | all         |

  @file_problem
  Scenario Outline: Use SD when a mandatory field in the config file is missing.
    Given the CLI is installed and ready to be executed
    And the CLI config file has lost the property <property_index>:
      | property |
      | url      |
      | username |
      | password |
    When I request the operation <operation_index>:
      | operation | arguments |
      | info      |           |
    Then the error contains the data <error_index>:
      | error_type   | message                                        |
      | [CLI Error]: | Configuration parameter "url" is required      |
      | [CLI Error]: | Configuration parameter "username" is required |
      | [CLI Error]: | Configuration parameter "password" is required |
    And the config file is restored

    Examples: 
      | property_index | cliconfig_index | error_index | operation_index |
      | 0              | 0               | 0           | 0               |
      | 1              | 0               | 1           | 0               |
      | 2              | 0               | 2           | 0               |

  @file_problem
  Scenario Outline: Use SD when the configuration file is corrupted with wrong data.
    Given the CLI is installed and ready to be executed
    And the CLI config file has been substituted
    When I request the operation <operation_index>:
      | operation | arguments |
      |           | -s        |
    Then the error contains the data <error_index>:
      | message                                                  |
      | Path to default config: (.*)                             |
      | Content of file:                                         |
      | Non valid file                                           |
    And the config file is restored

    Examples: 
      | operation_index | error_index |
      | 0               | all         |

  @file_problem
  Scenario Outline: Modify values in the config file.
    Given the CLI is installed and ready to be executed
    And the CLI config file is stored
    And the CLI is configured with the configuration <cliconfig_index>:
      | url    | username | password | verify | cert   | key    |
      | test   | [FILE]   | [FILE]   | [FILE] | [FILE] | [FILE] |
      | [FILE] | test     | [FILE]   | [FILE] | [FILE] | [FILE] |
      | [FILE] | [FILE]   | test     | [FILE] | [FILE] | [FILE] |
      | [FILE] | [FILE]   | [FILE]   | test   | [FILE] | [FILE] |
      | [FILE] | [FILE]   | [FILE]   | [FILE] | test   | [FILE] |
      | [FILE] | [FILE]   | [FILE]   | [FILE] | [FILE] | test   |
    When I request the operation <operation_index>:
      | operation | arguments |
      |           | -s        |
    Then the configuration contains the data <data_index>:
      | url    | username | password | verify | cert   | key    |
      | test   | [FILE]   | [FILE]   | [FILE] | [FILE] | [FILE] |
      | [FILE] | test     | [FILE]   | [FILE] | [FILE] | [FILE] |
      | [FILE] | [FILE]   | test     | [FILE] | [FILE] | [FILE] |
      | [FILE] | [FILE]   | [FILE]   | test   | [FILE] | [FILE] |
      | [FILE] | [FILE]   | [FILE]   | [FILE] | test   | [FILE] |
      | [FILE] | [FILE]   | [FILE]   | [FILE] | [FILE] | test   |
    And the config file is restored

    Examples: 
      | cliconfig_index | error_index | operation_index | data_index |
      | 0               | 0           | 0               | 0          |
      | 1               | 0           | 0               | 1          |
      | 2               | 0           | 0               | 2          |
      | 3               | 0           | 0               | 3          |
      | 4               | 0           | 0               | 4          |
      | 5               | 0           | 0               | 5          |
