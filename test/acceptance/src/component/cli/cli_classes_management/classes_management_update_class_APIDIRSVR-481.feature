# -*- coding: utf-8 -*-
Feature: CLI classes Management
  
    As an operation manager
    I want to configure the CLI client
    So that I can use the service directory with the desired configuration

  @update_class
  Scenario Outline: Update a class without mandatory params
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation      | arguments |
      |         | classes update |           |
      |         | classes update | test      |
    Then the result set contains the help info

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |
      | 0               | 0          | 1               | 0           |

  @update_class
  Scenario Outline: Update a class with invalid params
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation      | arguments         |
      |         | classes update | test2 wrong param |
    Then the error contains the data <error_index>:
      | error_type   | message                                        |
      | [CLI Error]: | <params> should match the format <key>=<value> |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @wrong_param @update_class
  Scenario Outline: Update class with repeated params
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation      | arguments                                                    |
      |         | classes update | test default_version=v1.0_update default_version=v1.0_update |
    Then the error contains the data <error_index>:
      | error_type   | message                     |
      | [CLI Error]: | default_version <key> can not be repeated |
      
     Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @update_class
  Scenario Outline: Update a whole class
    Given the CLI is installed and ready to be executed
    And the SD is ready to return a specific class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    And the SD is ready to return the updated class:
      | class_name | default_version | description                |
      | test       | v1.0_update     | This is an example updated |
    When I request the operation <operation_index>:
      | options | operation      | arguments                                                                |
      |         | classes update | test default_version=v1.0_update descritpion="This is an example update" |
    Then the result set contains the data <data_index>:
      | operation_type | operator | message |
      | Updated class: | test     | [EMPTY] |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @update_class
  Scenario Outline: Update a partially class
    Given the CLI is installed and ready to be executed
    And the SD is ready to return a specific class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    And the SD is ready to return the updated class:
      | class_name | default_version | description        |
      | test       | v1.0_update     | This is an example |
    When I request the operation <operation_index>:
      | options | operation      | arguments                        |
      |         | classes update | test default_version=v1.0_update |
    Then the result set contains the data <data_index>:
      | operation_type | operator | message |
      | Updated class: | test     | [EMPTY] |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @update_class
  Scenario Outline: Update the class_name
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation      | arguments            |
      |         | classes update | test class_name=fail |
    Then the error contains the data <error_index>:
      | error_type   | message                                 |
      | [CLI Error]: | "class_name" cannot be part of <params> |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @update_class
  Scenario Outline: Update with non existing params
    Given the CLI is installed and ready to be executed
    And the SD is ready to return a specific class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    And the SD is ready to return the updated class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    When I request the operation <operation_index>:
      | options | operation      | arguments              |
      |         | classes update | test non_existing=fail |
    Then the result set contains the data <data_index>:
      | operation_type | operator | message |
      | Updated class: | test     | [EMPTY] |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |
