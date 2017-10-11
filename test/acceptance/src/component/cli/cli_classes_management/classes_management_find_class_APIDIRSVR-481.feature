# -*- coding: utf-8 -*-
Feature: CLI classes Management
  
    As an operation manager
    I want to configure the CLI client
    So that I can use the service directory with the desired configuration

 
  @find_classes
  Scenario Outline: Find classes with serveral results
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the classes:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
      | test2      | v1.0            | This is an example |
    When I request the operation <operation_index>:
      | options | operation    | arguments |
      |         | classes find |           |
    Then the result set contains:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
      | test2      | v1.0            | This is an example |

    Examples: 
      | cliconfig_index | data_index | operation_index |
      | 0               | 0          | 0               |

  @find_classes
  Scenario Outline: Find classes with no results
    Given the CLI is installed and ready to be executed
    And the SD is ready to return no classes
    When I request the operation <operation_index>:
      | options | operation    | arguments |
      |         | classes find |           |
    Then the result set contains the data <data_index>:
      | operation_type | operator | message                                 |
      | [EMPTY]        | [EMPTY]  | No class matching these filter criteria |

    Examples: 
      | cliconfig_index | data_index | operation_index |
      | 0               | 0          | 0               |

