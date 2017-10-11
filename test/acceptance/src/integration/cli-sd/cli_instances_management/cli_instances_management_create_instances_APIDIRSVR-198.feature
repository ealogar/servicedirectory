# -*- coding: utf-8 -*-
Feature: CLI Endpoint Management
  
    As an operation manager
    I want to create, query and delete service instance
    So that I can modify the list of service endpoints available to Service Directory clients

  @happy_path @create_instance
  Scenario Outline: Create an instance with mandatory params
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    And a class is created with the CLI and operation values in <operation_index>:
      | options | operation      | arguments                      |
      |         | classes create | test v1.0 "This is an example" |
    And the SD is ready to return the instance:
      | id                       | version | url      | environment | class_name |
      | 5253d9a3fe813b07289be43c | v1.0    | www.test | production  | test       |
    And the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation        | arguments                                               |
      |         | instances create | test v1.0 www.test  [environment_failure_to_be_removed] |
    Then the result set contains the data <data_index>:
      | operation_type    | operator                 | message |
      | Created instance: | 5253d9a3fe813b07289be43c | [EMPTY] |
    And the SD in instances collection of class "test" has received the body <body_index>:
      | version | url      | environment                         | class_name |
      | v1.0    | www.test | [environment_failure_to_be_removed] | test       |

    Examples: 
      | cliconfig_index | data_index | operation_index | body_index |
      | 0               | 0          | 0               |   0        |
 @happy_path @create_instance
  Scenario Outline: Create an instance with mandatory params and optional
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    And a class is created with the CLI and operation values in <operation_index>:
      | options | operation      | arguments                      |
      |         | classes create | test v1.0 "This is an example" |
      |         | classes create | test v1.0 "This is an example" |
    And the SD is ready to return the instance <sd_config_index>:
      | id                       | version | url      | environment | class_name |
      | 5253d9a3fe813b07289be43a | v1.0    | www.test | production  | test       |
      | 5253d9a3fe813b07289be43b | v1.0    | www.test | production  | test       |
    And the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation        | arguments                                                         |
      |         | instances create | test v1.0 www.test production                                     |
      |         | instances create | test v1.0 www.test production attribute1=value1 attribute2=value2 |
    Then the result set contains the data <data_index>:
      | operation_type    | operator                 | message |
      | Created instance: | 5253d9a3fe813b07289be43a | [EMPTY] |
      | Created instance: | 5253d9a3fe813b07289be43b | [EMPTY] |
    And the SD in instances collection of class "test" has received the body <body_index>:
      | version | url      | environment                         | class_name | attributes                                    |
      | v1.0    | www.test | production                          | test       |                                               |
      | v1.0    | www.test | [environment_failure_to_be_removed] | test       | {"attribute1":"value1","attribute2":"value2"} |

    Examples: 
      | cliconfig_index | data_index | operation_index | sd_config_index | body_index |
      | 0               | 0          | 0               | 0               | 0          |
      | 0               | 1          | 1               | 1               | 1          |


  @wrong_params @create_instance
  Scenario Outline: Create an instance with missing mandatory params
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    And a class is created with the CLI and operation values in <operation_index>:
      | options | operation      | arguments                      |
      |         | classes create | test v1.0 "This is an example" |
      |         | classes create | test v1.0 "This is an example" |
      |         | classes create | test v1.0 "This is an example" |
    And the SD is ready to return the instance <sd_config_index>:
      | id                       | version | url      | environment | class_name |
      | 5253d9a3fe813b07289be43a | v1.0    | www.test | production  | test       |
    And the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation        | arguments |
      |         | instances create |           |
      |         | instances create | test      |
      |         | instances create | test v1.0 |
    Then the result set contains the help info

    Examples: 
      | cliconfig_index | data_index | operation_index | sd_config_index |
      | 0               | 0          | 0               | 0               |
      | 0               | 0          | 1               | 0               |
      | 0               | 0          | 2               | 0               |

  @wrong_params @create_instance
  Scenario Outline: Create an instance with valid special characters
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    And a class is created with the CLI and operation values in <operation_index>:
      | options | operation      | arguments                      |
      |         | classes create | test v1.0 "This is an example" |
      |         | classes create | test v1.0 "This is an example" |
      |         | classes create | test v1.0 "This is an example" |
      |         | classes create | test v1.0 "This is an example" |
      |         | classes create | test v1.0 "This is an example" |
    And the SD is ready to return the instance <sd_config_index>:
      | id                       | version | url       | environment | class_name |
      | 5253d9a3fe813b07289be43a | v1.0ñ   | www.test  | production  | test       |
      | 5253d9a3fe813b07289be43b | v1.0    | www.testñ | production  | test       |
      | 5253d9a3fe813b07289be43c | v1.0    | www.test  | productionñ | test       |
      | 5253d9a3fe813b07289be43d | v1.0    | www.test  | production  | test       |
      | 5253d9a3fe813b07289be43e | v1.0    | www.test  | production  | test       |
      | 5253d9a3fe813b07289be43f | v1.0    | www.test  | production  | test       |
    And the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation        | arguments                                                          |
      |         | instances create | test v1.0ñ www.test production attribute1=value1 attribute2=value2 |
      |         | instances create | test v1.0 www.testñ production attribute1=value1 attribute2=value2 |
      |         | instances create | test v1.0 www.test productionñ attribute1=value1 attribute2=value2 |
      |         | instances create | test v1.0 www.test production attribute1ñ=value1 attribute2=value2 |
      |         | instances create | test v1.0 www.test production attribute1=value1ñ attribute2=value2 |
    Then the result set contains the data <data_index>:
      | operation_type    | operator                 | message |
      | Created instance: | 5253d9a3fe813b07289be43a | [EMPTY] |
      | Created instance: | 5253d9a3fe813b07289be43b | [EMPTY] |
      | Created instance: | 5253d9a3fe813b07289be43c | [EMPTY] |
      | Created instance: | 5253d9a3fe813b07289be43d | [EMPTY] |
      | Created instance: | 5253d9a3fe813b07289be43e | [EMPTY] |

    Examples: 
      | cliconfig_index | data_index | operation_index | sd_config_index |
      | 0               | 0          | 0               | 0               |
      | 0               | 1          | 1               | 1               |
      | 0               | 2          | 2               | 2               |
      | 0               | 3          | 3               | 3               |
      | 0               | 4          | 4               | 4               |

  @error_management @create_instance
  Scenario Outline: Create an instance with and error 400 returned
    Given the CLI is installed and ready to be executed
    And the SD is ready to return an error 400 for instance creation:
      | exceptionId | exceptionText                                                                                       |
      | SVC1021     | Invalid parameter value: http://endpoint.tid.es-v1.0. Supported values are: non-duplicated-instance |
    When I request the operation <operation_index>:
      | options | operation        | arguments                                              |
      |         | instances create | test v1.0 www.test [environment_failure_to_be_removed] |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText                                                                                       |
      | [SD Error]: | SVC1021     | Invalid parameter value: http://endpoint.tid.es-v1.0. Supported values are: non-duplicated-instance |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @error_management @create_instance
  Scenario Outline: Create a class with and error 500 returned
    Given the CLI is installed and ready to be executed
    And the SD is ready to return an error 500 for instance creation:
      | exceptionId | exceptionText            |
      | SVR1000     | Generic Server Error(.*) |
    When I request the operation <operation_index>:
      | options | operation        | arguments                                              |
      |         | instances create | test v1.0 www.test [environment_failure_to_be_removed] |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText            |
      | [SD Error]: | SVR1000     | Generic Server Error(.*) |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @error_management @create_instance
  Scenario Outline: Create a class with and error 403 returned
    Given the CLI is installed and ready to be executed
    And the SD is ready to return an error 403 for instance creation:
      | exceptionId | exceptionText |
      | POL0011     | (.*)          |
    When I request the operation <operation_index>:
      | options | operation        | arguments                                              |
      |         | instances create | test v1.0 www.test [environment_failure_to_be_removed] |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText |
      | [SD Error]: | POL0011     | (.*)          |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @error_management @create_instance
  Scenario Outline: Create a class with and error 405 returned
    Given the CLI is installed and ready to be executed
    And the SD is ready to return an error 405 for instance creation:
      | exceptionId | exceptionText                           |
      | SVC1003     | Requested Operation does not exist: PUT |
    When I request the operation <operation_index>:
      | options | operation        | arguments                                              |
      |         | instances create | test v1.0 www.test [environment_failure_to_be_removed] |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText                           |
      | [SD Error]: | SVC1003     | Requested Operation does not exist: PUT |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @happy_path @find_instances
  Scenario Outline: Find all the instances of a existing class
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the following instances of class "test":
      | id                       | version | url      | environment | class_name |
      | 5253d9a3fe813b07289be431 | v1.1    | www.test | production  | test       |
      | 5253d9a3fe813b07289be432 | v1.2    | www.test | production  | test       |
      | 5253d9a3fe813b07289be433 | v1.3    | www.test | production  | test       |
    When I request the operation <operation_index>:
      | options | operation      | arguments |
      |         | instances find | test      |
    Then the result set contains:
      | id                       | version | url      | environment | class_name |
      | 5253d9a3fe813b07289be431 | v1.1    | www.test | production  | test       |
      | 5253d9a3fe813b07289be432 | v1.2    | www.test | production  | test       |
      | 5253d9a3fe813b07289be433 | v1.3    | www.test | production  | test       |

    Examples: 
      | operation_index |
      | 0               |

  @happy_path @find_instances
  Scenario Outline: Find all the instances of a existing class and no results
    Given the CLI is installed and ready to be executed
    And the SD is ready to return no instances of class "test"
    When I request the operation <operation_index>:
      | options | operation      | arguments |
      |         | instances find | test      |
    Then the result set contains the data <data_index>:
      | operation_type | operator | message                                    |
      | [EMPTY]        | [EMPTY]  | No instance matching these filter criteria |

    Examples: 
      | data_index | operation_index |
      | 0          | 0               |

  @happy_path @find_instances
  Scenario Outline: Find all the instances of a existing class filtered with params
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the following instances of class "test":
      | id                       | version | url       | environment | class_name |
      | 5253d9a3fe813b07289be431 | v1.1    | www.test1 | production  | test       |
      | 5253d9a3fe813b07289be432 | v1.1    | www.test2 | production  | test       |
      | 5253d9a3fe813b07289be433 | v1.1    | www.test3 | production  | test       |
    When I request the operation <operation_index>:
      | options | operation      | arguments                                |
      |         | instances find | test version=v1.1 environment=production |
    Then the result set contains:
      | id                       | version | url       | environment | class_name |
      | 5253d9a3fe813b07289be431 | v1.1    | www.test1 | production  | test       |
      | 5253d9a3fe813b07289be432 | v1.1    | www.test2 | production  | test       |
      | 5253d9a3fe813b07289be433 | v1.1    | www.test3 | production  | test       |
    And the SD in instances collection of class "test" has received the params <param_index>:
      | version      | environment            |
      | version=v1.1 | environment=production |

    Examples: 
      | operation_index | param_index |
      | 0               | 0           |

  @missing_parama @find_instances
  Scenario Outline: Find all the instances of a existing class with missing paramas
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation      | arguments |
      |         | instances find |           |
    Then the result set contains the help info

    Examples: 
      | operation_index |
      | 0               |
      
  @wrong_param @find_instances
  Scenario Outline: Find all the instances of a existing class with wrong params
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation      | arguments      |
      |         | instances find | test test test |
    Then the error contains the data <error_index>:
      | error_type   | message                                        |
      | [CLI Error]: | <params> should match the format <key>=<value> |

    Examples: 
      | operation_index | error_index |
      | 0               | 0           |

  @happy_path @get_instances
  Scenario Outline: Get a instances of a existing class
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version | url      | environment | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1    | www.test | production  | test       | {"key":"value"} |
    When I request the operation <operation_index>:
      | options | operation     | arguments                     |
      |         | instances get | test 5253d9a3fe813b07289be431 |
    Then the result set contains the item <data_index>:
      | id                       | version | url      | environment | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1    | www.test | production  | test       | {"key":"value"} |

    Examples: 
      | operation_index | data_index |
      | 0               | 0          |

  @missing_params @get_instances
  Scenario Outline: Get a instances with extra or missing params
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version | url      | environment | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1    | www.test | production  | test       | {"key":"value"} |
    When I request the operation <operation_index>:
      | options | operation     | arguments                           |
      |         | instances get | test 5253d9a3fe813b07289be431 extra |
      |         | instances get |                                     |
      |         | instances get | test                                |
    Then the result set contains the help info

    Examples: 
      | operation_index |
      | 0               |
      | 1               |
 