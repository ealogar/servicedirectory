# -*- coding: utf-8 -*-
Feature: CLI classes Management
  
    As an operation manager
    I want to configure the CLI client
    So that I can use the service directory with the desired configuration

 
  @delete_class
  Scenario Outline: Delete a class
    Given the CLI is installed and ready to be executed
    And the SD is ready to accept the deletion of resource <sd_config_index>:
      | resource           |
      | sd/v1/classes/test |
    When I request the operation <operation_index>:
      | options | operation      | arguments |
      |         | classes delete | test      |
    Then the result set contains the data <data_index>:
      | operation_type | operator | message |
      | Deleted class: | test     | [EMPTY] |

    Examples: 
      | sd_config_index | data_index | operation_index |
      | 0               | 0          | 0               |

  @delete_class
  Scenario Outline: Delete of non existing class
    Given the CLI is installed and ready to be executed
    And the SD is ready to return an error 404 in the class:
      | exceptionId | exceptionText                |
      | SVC1006     | Resource test does not exist |
    When I request the operation <operation_index>:
      | options | operation      | arguments |
      |         | classes delete | test      |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText                |
      | [SD Error]: | SVC1006     | Resource test does not exist |

    Examples: 
      | sd_config_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @delete_class
  Scenario Outline: Delete a class with non supported params
    Given the CLI is installed and ready to be executed
    And the SD is ready to accept the deletion of resource <sd_config_index>:
      | resource           |
      | sd/v1/classes/test |
    When I request the operation <operation_index>:
      | options | operation      | arguments         |
      |         | classes delete | test non suported |
    Then the result set contains the help info

    Examples: 
      | sd_config_index | data_index | operation_index |
      | 0               | 0          | 0               |

  @delete_class
  Scenario Outline: Delete a class without mandatory supported params
    Given the CLI is installed and ready to be executed
    And the SD is ready to accept the deletion of resource <sd_config_index>:
      | resource           |
      | sd/v1/classes/test |
    When I request the operation <operation_index>:
      | options | operation      | arguments |
      |         | classes delete |           |
    Then the result set contains the help info

    Examples: 
      | sd_config_index | data_index | operation_index |
      | 0               | 0          | 0               |

  