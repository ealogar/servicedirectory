# -*- coding: utf-8 -*-
Feature: CLI Endpoint Management
  
    As an operation manager
    I want to create, query and delete service instance
    So that I can modify the list of service endpoints available to Service Directory clients

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

  @wrong_param @find_instances
  Scenario Outline: Update instances with repeated params
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation      | arguments        |
      |         | instances find | test key=a key=a |
    Then the error contains the data <error_index>:
      | error_type   | message                     |
      | [CLI Error]: | key <key> can not be repeated |

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
