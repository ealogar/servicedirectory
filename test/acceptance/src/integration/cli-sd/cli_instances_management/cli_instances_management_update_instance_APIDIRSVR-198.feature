# -*- coding: utf-8 -*-
Feature: CLI Endpoint Management
  
    As an operation manager
    I want to create, query and delete service instance
    So that I can modify the list of service endpoints available to Service Directory clients

  @happy_path @update_instance
  Scenario Outline: Update an existing instance with base attributes
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version      | url              | environment        | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1_updated | www.test_updated | production_updated | test       | {"key":"value"} |
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version      | url              | environment        | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1_updated | www.test_updated | production_updated | test       | {"key":"value"} |
    When I request the operation <operation_index>:
      | options | operation        | arguments                                                                                              |
      |         | instances update | test 5253d9a3fe813b07289be431 version=v1.1_updated                                                     |
      |         | instances update | test 5253d9a3fe813b07289be431 version=v1.1_updated url=www.test_updated                                |
      |         | instances update | test 5253d9a3fe813b07289be431 version=v1.1_updated url=www.test_updated environment=production_updated |
    Then the result set contains the data <data_index>:
      | operation_type    | operator                 | message |
      | Updated instance: | 5253d9a3fe813b07289be431 | [EMPTY] |

    Examples: 
      | operation_index | sd_config_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |
      | 1               | 0               | 0          | 0           |
      | 2               | 0               | 0          | 0           |

  @wrong_params @update_instance
  Scenario Outline: Update an existing instance with base wrong attributes
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version      | url              | environment        | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1_updated | www.test_updated | production_updated | test       | {"key":"value"} |
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version      | url              | environment        | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1_updated | www.test_updated | production_updated | test       | {"key":"value"} |
    When I request the operation <operation_index>:
      | options | operation        | arguments                                             |
      |         | instances update | test 5253d9a3fe813b07289be431 v1.1_updated            |
      |         | instances update | test 5253d9a3fe813b07289be431 class_name=v1.1_updated |
    Then the error contains the data <error_index>:
      | error_type   | message                                        |
      | [CLI Error]: | <params> should match the format <key>=<value> |
      | [CLI Error]: | "class_name" cannot be part of <params>        |

    Examples: 
      | operation_index | sd_config_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |
      | 1               | 0               | 0          | 0           |

  @missing_param @update_instance
  Scenario Outline: Update an existing instance with missing attributes
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version      | url              | environment        | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1_updated | www.test_updated | production_updated | test       | {"key":"value"} |
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version      | url              | environment        | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1_updated | www.test_updated | production_updated | test       | {"key":"value"} |
    When I request the operation <operation_index>:
      | options | operation        | arguments                     |
      |         | instances update |                               |
      |         | instances update | test                          |
      |         | instances update | test 5253d9a3fe813b07289be431 |
    Then the result set contains the help info

    Examples: 
      | operation_index | sd_config_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |
      | 1               | 0               | 0          | 0           |
      | 2               | 0               | 0          | 0           |

  @happy_path @update_instance
  Scenario Outline: Update an existing instance with new attributes
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version      | url              | environment        | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1_updated | www.test_updated | production_updated | test       | {"key":"value"} |
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version      | url              | environment        | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1_updated | www.test_updated | production_updated | test       | {"key":"value"} |
    When I request the operation <operation_index>:
      | options | operation        | arguments                                                                                              |
      |         | instances update-attrs | test 5253d9a3fe813b07289be431 key=new_value                                                     |
      |         | instances update-attrs | test 5253d9a3fe813b07289be431 key_new=new_value                                |
      |         | instances update-attrs | test 5253d9a3fe813b07289be431 key=new_value key_new=new_value |
    Then the result set contains the data <data_index>:
      | operation_type    | operator                 | message |
      | Updated instance attributes: | 5253d9a3fe813b07289be431 | [EMPTY] |

    Examples: 
      | operation_index | sd_config_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |
      | 1               | 0               | 0          | 0           |
      | 2               | 0               | 0          | 0           |

  @wrong_params @update_instance
  Scenario Outline: Update an existing instance with wrong attributes
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version      | url              | environment        | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1_updated | www.test_updated | production_updated | test       | {"key":"value"} |
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version      | url              | environment        | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1_updated | www.test_updated | production_updated | test       | {"key":"value"} |
    When I request the operation <operation_index>:
      | options | operation        | arguments                                             |
      |         | instances update-attrs | test 5253d9a3fe813b07289be431 v1.1_updated            |
      |         | instances update-attrs | test 5253d9a3fe813b07289be431 class_name=v1.1_updated |
    Then the error contains the data <error_index>:
      | error_type   | message                                        |
      | [CLI Error]: | <params> should match the format <key>=<value> |
      | [CLI Error]: | "class_name" cannot be part of <params>        |

    Examples: 
      | operation_index | sd_config_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |
      | 1               | 0               | 0          | 0           |

  @missing_param @update_instance
  Scenario Outline: Update an existing instance with missing params
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version      | url              | environment        | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1_updated | www.test_updated | production_updated | test       | {"key":"value"} |
    And the SD is ready to return the instance 5253d9a3fe813b07289be431 of class "test":
      | id                       | version      | url              | environment        | class_name | attributes      |
      | 5253d9a3fe813b07289be431 | v1.1_updated | www.test_updated | production_updated | test       | {"key":"value"} |
    When I request the operation <operation_index>:
      | options | operation        | arguments                     |
      |         | instances update-attrs |                               |
      |         | instances update-attrs | test                          |
      |         | instances update-attrs | test 5253d9a3fe813b07289be431 |
    Then the result set contains the help info

    Examples: 
      | operation_index | sd_config_index | data_index | error_index |
      | 0               | 0               | 0          | 0           |
      | 1               | 0               | 0          | 0           |
      | 2               | 0               | 0          | 0           |
