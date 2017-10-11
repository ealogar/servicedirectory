# -*- coding: utf-8 -*-
Feature: CLI classes Management
  
    As an operation manager
    I want to configure the CLI client
    So that I can use the service directory with the desired configuration

  @happy_path @create_class
  Scenario Outline: Create a class with valid mandatory data
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the class:
      | class_name | default_version |
      | test       | v1.0            |
    When I request the operation <operation_index>:
      | options | operation      | arguments |
      |         | classes create | test v1.0 |
    Then the result set contains the data <data_index>:
      | operation_type | operator | message |
      | Created class: | test     | [EMPTY] |

    Examples: 
      | cliconfig_index | data_index | operation_index |
      | 0               | 0          | 0               |

  @create_class
  Scenario Outline: Create a class with valid mandatory and optional data
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    When I request the operation <operation_index>:
      | options | operation      | arguments                      |
      |         | classes create | test v1.0 "This is an example" |
    Then the result set contains the data <data_index>:
      | operation_type | operator | message |
      | Created class: | test     | [EMPTY] |

    Examples: 
      | cliconfig_index | data_index | operation_index |
      | 0               | 0          | 0               |

  @create_class
  Scenario Outline: Create a class with extra data not suported
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the class:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    When I request the operation <operation_index>:
      | options | operation      | arguments           |
      |         | classes create | test v1.0 test test |
    Then the result set contains the help info

    Examples: 
      | cliconfig_index | data_index | operation_index |
      | 0               | 0          | 0               |

  @create_class
  Scenario Outline: Create a class with and error 400 returned
    Given the CLI is installed and ready to be executed
    And the SD is ready to return an error 400:
      | exceptionId | exceptionText                       |
      | SVC0002     | Invalid parameter value: class_name |
    When I request the operation <operation_index>:
      | options | operation      | arguments      |
      |         | classes create | test v1.0 test |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText                       |
      | [SD Error]: | SVC0002     | Invalid parameter value: class_name |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @create_class
  Scenario Outline: Create a class with and error 500 returned
    Given the CLI is installed and ready to be executed
    And the SD is ready to return an error 500:
      | exceptionId | exceptionText            |
      | SVR1000     | Generic Server Error(.*) |
    When I request the operation <operation_index>:
      | options | operation      | arguments      |
      |         | classes create | test v1.0 test |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText            |
      | [SD Error]: | SVR1000     | Generic Server Error(.*) |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @create_class
  Scenario Outline: Create a class with and error 403 returned
    Given the CLI is installed and ready to be executed
    And the SD is ready to return an error 403:
      | exceptionId | exceptionText |
      | POL0011     | (.*)          |
    When I request the operation <operation_index>:
      | options | operation      | arguments      |
      |         | classes create | test v1.0 test |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText |
      | [SD Error]: | POL0011     | (.*)          |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @create_class
  Scenario Outline: Create a class with and error 405 returned
    Given the CLI is installed and ready to be executed
    And the SD is ready to return an error 405:
      | exceptionId | exceptionText                           |
      | SVC1003     | Requested Operation does not exist: PUT |
    When I request the operation <operation_index>:
      | options | operation      | arguments      |
      |         | classes create | test v1.0 test |
    Then the error contains the data <error_index>:
      | error_type  | exceptionId | exceptionText                           |
      | [SD Error]: | SVC1003     | Requested Operation does not exist: PUT |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @create_class
  Scenario Outline: Create a class when the SD is not available
    Given the CLI is installed and ready to be executed
    When I request the operation <operation_index>:
      | options | operation | arguments |
      |         | info      |           |
    Then the error contains the data <error_index>:
      | error_type   | message                                                                                                             |
      | [CLI Error]: | There is no connection currently to Service Directory. Try again later or contact Service directory support service |

    Examples: 
      | cliconfig_index | data_index | operation_index | error_index |
      | 0               | 0          | 0               | 0           |

  @create_class
  Scenario Outline: Request info when the SD response is and invalid format
    Given the CLI is installed and ready to be executed
    And the SD is ready to return an invalid data for resources in <invalid_index>:
      | resource      | data           |
      | sd/v1/classes | [BAD_DATA]     |
      | sd/v1/classes | [CORRUPT_DATA] |
      | sd/v1/classes | [BLANK_DATA]   |
      | sd/v1/classes | [EMPTY_DATA]   |
    When I request the operation <operation_index>:
      | options | operation      | arguments                      |
      |         | classes create | test v1.0 "This is an example" |
    Then the error contains the data <error_index>:
      | error_type   | message                                                                                                                    |
      | [CLI Error]: | Service Directory is not responding properly to your request. Try again later or contact Service directory support service |

    Examples: 
      | invalid_index | data_index | operation_index | error_index |
      | 0             | 0          | 0               | 0           |
      | 1             | 0          | 0               | 0           |
      | 2             | 0          | 0               | 0           |
      | 3             | 0          | 0               | 0           |

  @create_class
  Scenario Outline: Create a class with a long time to wait
    Given the CLI is installed and ready to be executed
    And the SD is ready to return the class with timeout 2:
      | class_name | default_version | description        |
      | test       | v1.0            | This is an example |
    When I request the operation <operation_index>:
      | options | operation      | arguments                      |
      |         | classes create | test v1.0 "This is an example" |
    Then the result set contains the data <data_index>:
      | operation_type | operator | message |
      | Created class: | test     | [EMPTY] |

    Examples: 
      | cliconfig_index | data_index | operation_index |
      | 0               | 0          | 0               |

  