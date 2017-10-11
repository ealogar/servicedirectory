# -*- coding: utf-8 -*-
Feature: CLI Endpoint Management
  
    As an operation manager
    I want to create, query and delete service instance
    So that I can modify the list of service endpoints available to Service Directory clients

 @happy_path @delete_instance
  Scenario Outline: Delete an instance
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    And a class is created with the CLI and operation values in <operation_index>:
      | options | operation      | arguments                      |
      |         | classes create | test v1.0 "This is an example" |
    And the CLI is installed and ready to be executed
    And the SD is ready to return the instance:
      | id                       | version | url      | environment | class_name |
      | 5253d9a3fe813b07289be43c | v1.0    | www.test | production  | test       |
    And an instance is created with the CLI and operation values in <operation_index>:
      | options | operation        | arguments                                              |
      |         | instances create | test v1.0 www.test [environment_failure_to_be_removed] |
    And the CLI is installed and ready to be executed
    And the SD is ready to accept the deletion of resource <sd_config_index>:
      | resource                                              |
      | sd/v1/classes/test/instances/5253d9a3fe813b07289be43c |
    When I request the operation <operation_index>:
      | options | operation        | arguments                     |
      |         | instances delete | test 5253d9a3fe813b07289be43c |
    Then the result set contains the data <data_index>:
      | operation_type    | operator                                | message |
      | Deleted instance: | 5253d9a3fe813b07289be43c in class: test | [EMPTY] |

    Examples: 
      | operation_index | sd_config_index | data_index |
      | 0               | 0               | 0          |

  @resource_not_found @delete_instance
  Scenario Outline: Delete an instance over a non existing class
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    And a class is created with the CLI and operation values in <operation_index>:
      | options | operation      | arguments                      |
      |         | classes create | test v1.0 "This is an example" |
    And the CLI is installed and ready to be executed
    And the SD is ready to return the instance:
      | id                       | version | url      | environment | class_name |
      | 5253d9a3fe813b07289be43c | v1.0    | www.test | production  | test       |
    And an instance is created with the CLI and operation values in <operation_index>:
      | options | operation        | arguments                                              |
      |         | instances create | test v1.0 www.test [environment_failure_to_be_removed] |
    And the CLI is installed and ready to be executed
    And the SD is ready to return an error 404 in the instance 5253d9a3fe813b07289be43c of class test:
      | exceptionId | exceptionText                |
      | SVC1006     | Resource test does not exist |
    When I request the operation <operation_index>:
      | options | operation        | arguments                     |
      |         | instances delete | test 5253d9a3fe813b07289be43c |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText                |
      | [SD Error]: | SVC1006     | Resource test does not exist |

    Examples: 
      | operation_index | sd_config_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |

  @resource_not_found @delete_instance
  Scenario Outline: Delete an non exisitng instance over an existing class
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    And a class is created with the CLI and operation values in <operation_index>:
      | options | operation      | arguments                      |
      |         | classes create | test v1.0 "This is an example" |
    And the CLI is installed and ready to be executed
    And the SD is ready to return an error 404 in the instance 5253d9a3fe813b07289be43c of class test:
      | exceptionId | exceptionText                                    |
      | SVC1006     | Resource 5253d9a3fe813b07289be43c does not exist |
    When I request the operation <operation_index>:
      | options | operation        | arguments                     |
      |         | instances delete | test 5253d9a3fe813b07289be43c |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText                                    |
      | [SD Error]: | SVC1006     | Resource 5253d9a3fe813b07289be43c does not exist |

    Examples: 
      | operation_index | sd_config_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |

  @resource_not_found @delete_instance
  Scenario Outline: Delete an exisitng instance that does not belong to an existing class
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    And a class is created with the CLI and operation values in <operation_index>:
      | options | operation      | arguments                      |
      |         | classes create | test v1.0 "This is an example" |
    And the CLI is installed and ready to be executed
    And the SD is ready to return the instance:
      | id                       | version | url      | environment | class_name |
      | 5253d9a3fe813b07289be43c | v1.0    | www.test | production  | test       |
    And an instance is created with the CLI and operation values in <operation_index>:
      | options | operation        | arguments                                              |
      |         | instances create | test v1.0 www.test [environment_failure_to_be_removed] |
    And the CLI is installed and ready to be executed
    And the SD is ready to return the class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    And a class is created with the CLI and operation values in <operation_index>:
      | options | operation      | arguments                       |
      |         | classes create | test2 v1.0 "This is an example" |
    And the CLI is installed and ready to be executed
    And the SD is ready to return an error 404 in the instance 5253d9a3fe813b07289be43c of class test2:
      | exceptionId | exceptionText                                                                                    |
      | SVC1021     | Invalid parameter value: test-5253d9a3fe813b07289be43c. Supported values are: instances-of-class |
    When I request the operation <operation_index>:
      | options | operation        | arguments                      |
      |         | instances delete | test2 5253d9a3fe813b07289be43c |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText                                                                                    |
      | [SD Error]: | SVC1021     | Invalid parameter value: test-5253d9a3fe813b07289be43c. Supported values are: instances-of-class |

    Examples: 
      | operation_index | sd_config_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |

  @resource_not_found @delete_instance
  Scenario Outline: Delete an instance with missing or extra params
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation        | arguments                           |
      |         | instances delete |                                     |
      |         | instances delete | test                                |
      |         | instances delete | test 5253d9a3fe813b07289be43c extra |
    Then the result set contains the help info

    Examples: 
      | operation_index |
      | 0               |
      | 1               |
      | 2               |