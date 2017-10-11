# -*- coding: utf-8 -*-
Feature: CLI Endpoint Management
  
    As an operation manager
    I want to configure the CLI client
    So that I can use the service directory with the desired configuration

  Scenario Outline: Display version name
    Given the CLI is installed and ready to be executed
    Given the SD is ready to return the version info:
      | app_name          | default_version |
      | Service Directory | v1              |
    And the CLI is configured with the configuration <cliconfig_index>:
      | url    | username | password | verify | cert   | key    |
      | [FILE] | [FILE]   | [FILE]   | [FILE] | [FILE] | [FILE] |
    When I request the operation <operation_index>:
      | options | operation | arguments |
      |         | info      |           |
    Then the result set contains the data <data_index>:
      | operation_type | operator | app_name          | default_version | message |
      | [EMPTY]        | [EMPTY]  | Service Directory | v1              | [EMPTY] |

    Examples: 
      | cliconfig_index | data_index | operation_index |
      | 0               | 0          | 0               |
