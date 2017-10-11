# -*- coding: utf-8 -*-
Feature: class Publication
  
  As a class provider
  I want to publish my class information in the SD
  so that I can add different instances exposing this class to be discovered and used.

  @happy_path
  Scenario Outline: Publication of a new class with valid mandatory data_TDAFBA-464
    Given the DB has no classes already published
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data <class_index>:
      | class_name                   | default_version                 |
      | n                            | v                               |
      | Complex_default_version      | v57.12.12.110b-unstable         |
      | Symbols                      | 1.0-131(b)                      |
      | Non-ASCII                    | á.é.í                           |
      | [STRING_WITH_LENGTH_511]     | under_boundary_value_class_name |
      | [STRING_WITH_LENGTH_512]     | boundary_value_class_name       |
      | under_boundary_value_version | [STRING_WITH_LENGTH_255]        |
      | boundary_value_version       | [STRING_WITH_LENGTH_256]        |
    Then I get a success response of type 201 with location <location_index>:
      | location                                                                                                                       |
      | $base_api_url/$classes_url/n                                                                                                   |
      | $base_api_url/$classes_url/Complex_default_version |
      | $base_api_url/$classes_url/Symbols                                                                                             |
      | $base_api_url/$classes_url/Non-ASCII                                                                                           |
      | $base_api_url/$classes_url/$class_name                                                                                         |
      | $base_api_url/$classes_url/under_boundary_value_version                                                                        |
      | $base_api_url/$classes_url/boundary_value_version                                                                              |
    And the response contains the class data
    And the location returns the class data

    Examples: 
      | class_index | location_index |
      | 0           | 0              |
      | 1           | 1              |
      | 2           | 2              |
      | 3           | 3              |
      | 4           | 4              |
      | 5           | 4              |
      | 6           | 5              |
      | 7           | 6              |

  @happy_path
  Scenario Outline: Publication of a new class with valid mandatory and optional data_TDAFBA-465
    Given the DB has no classes already published
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data <class_index>:
      | class_name                       | description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | default_version |
      | Empty-desc                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | v1.0             |
      | Short-desc                       | d                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | v1.0             |
      | Long-desc-different-lines        | Long description which contains a small story in several lines.\nEvery Sunday, the birds go to their bird church. All the birds in that parish go there. Starlings, eagles, pigeons, sparrows, blackbirds, ducks, geese, and so on.\nThe birds enter the church. Gravely, silently, they file into the church and find their way to their seats in the wooden church pews.\nMusic plays. Then, the bird preacher enters the room, using a small door behind the main altar. The bird preacher makes a dramatic gesture. Then he clears his throat and addresses his congregation. | v1.0             |
      | under_boundary_value_description | [STRING_WITH_LENGTH_1023]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | v1.0             |
      | boundary_value_description       | [STRING_WITH_LENGTH_1024]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | v1.0             |
      | Symbols-desc                     | +*=.,;"'@#$%()/\\?!                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | v1.0             |
      | Non-ASCII-desc                   | ñçüúóíéá                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | v1.0             |
    Then I get a success response of type 201 with location <location_index>:
      | location                                                    |
      | $base_api_url/$classes_url/Empty-desc                       |
      | $base_api_url/$classes_url/Short-desc                       |
      | $base_api_url/$classes_url/Long-desc                        |
      | $base_api_url/$classes_url/under_boundary_value_description |
      | $base_api_url/$classes_url/boundary_value_description       |
      | $base_api_url/$classes_url/Symbols-desc                     |
      | $base_api_url/$classes_url/Non-ASCII-desc                   |
    And the response contains the class data
    And the location returns the class data

    Examples: 
      | class_index | location_index |
      | 0           | 0              |
      | 1           | 1              |
      | 2           | 2              |
      | 3           | 3              |
      | 4           | 4              |
      | 5           | 5              |
      | 6           | 6              |

  @method_not_allowed
  Scenario Outline: Publication of a class with wrong method
    Given the DB has no classes already published
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I try to put in $base_api_url/$classes_url the class data <class_index>:
      | class_name | description | default_version |
      | class      | class       | v1.0             |
    Then I get an error response of type 405 with error code SVC1003
    And the exceptionText contains <exceptionText_index>
      | exceptionText                           |
      | Requested Operation does not exist:(.*) |

    Examples: 
      | class_index | exceptionText_index |
      | 0           | 0                   |

  @internal_error @local
  Scenario Outline: Publication of a class when the DB is down_TDAFBA-469
    Given the DB has stopped working
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data <class_index>:
      | class_name | description | default_version |
      | class      | class       | v1.0             |
    Then I get an error response of type 500 with error code SVR1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText            |
      | Generic Server Error(.*) |

    Examples: 
      | class_index | exceptionText_index |
      | 0           | 0                   |

  @malformed_request
  Scenario Outline: Publication of a new class using unstructured data_TDAFBA-467
    Given the DB has no classes already published
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the data UNSTRUCTURED_DATA
    Then I get an error response of type 403 with error code POL0011
    And the exceptionText contains <exceptionText_index>:
      | exceptionText                                |
      | Media type (.*) not supported |

    Examples: 
      | exceptionText_index |
      | 0                   |

  @malformed_request
  Scenario Outline: Publication of a new class using malformed data
    Given the DB has no classes already published
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the data MALFORMED_DATA
    Then I get an error response of type 400 with error code SVC1023
    And the exceptionText contains <exceptionText_index>
      | exceptionText                              |
      | Parser Error: (.*) content not well formed |

    Examples: 
      | exceptionText_index |
      | 0                   |

  @missing_mandatory
  Scenario Outline: Publication of a new class with missing mandatory data
    Given the DB has no classes already published
    And the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data <class_index>:
      | class_name      | default_version |
      | [MISSING_PARAM] | v1.0             |
      | class           | [MISSING_PARAM] |
    Then I get an error response of type 400 with error code SVC1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText                    |
      | Missing mandatory parameter:(.*) |

    Examples: 
      | class_index | exceptionText_index |
      | 0           | 0                   |
      | 1           | 0                   |

  @parameters_validation
  Scenario Outline: Publication of a new class with invalid mandatory data_TDAFBA-466
    Given the DB has no classes already published
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data <class_index>:
      | class_name                        | default_version                |
      | Name with spaces                  | v1.0                            |
      | Name.with.symbols                 | v1.0                            |
      | Name_Nón-ASCII                    | v1.0                            |
      | non_valid_set1_ºª\\!"·$%&/()=?¿'¡ | v1.0                            |
      | non_valid_set2_;:,´¨{}[]^`*+_><   | v1.0                            |
      |                                   | empty_name                     |
      | empty_version                     |                                |
      | [STRING_WITH_LENGTH_513]          | over_boundary_value_class_name |
      | over_boundary_value_version       | [STRING_WITH_LENGTH_257]       |
      | not_string_default_version       | 1.0      |
      | 1.0       | not_string_class_name      |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                 |
      | Invalid parameter value: (.*) |

    Examples: 
      | class_index | exceptionText_index |
      | 0           | 0                   |
      | 1           | 0                   |
      | 2           | 0                   |
      | 3           | 0                   |
      | 4           | 0                   |
      | 5           | 0                   |
      | 6           | 0                   |
      | 7           | 0                   |
      | 8           | 0                   |
      | 9           | 0                   |
      | 10           | 0                   |

  @parameters_validation
  Scenario Outline: Publication of a new class with invalid optional data_TDAFBA-466
    Given the DB has no classes already published
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$classes_url the class data <class_index>:
      | class_name                      | default_version | description               |
      | over_boundary_value_description | v1.0             | [STRING_WITH_LENGTH_1025] |
      | no_string_description | v1.0             | 1.0 |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                 |
      | Invalid parameter value: (.*) |

    Examples: 
      | class_index | exceptionText_index |
      | 0           | 0                   |
      | 1           | 0                   |

  @existing_resource
  Scenario Outline: Publication of a class with a name already used_TDAFBA-468
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | class      | class       | v1.0             |
    When I send to $base_api_url/$classes_url the class data <class_index>:
      | class_name | description | default_version |
      | class      | class       | v1.0             |
      | class      | New class   | v2.0             |
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                                           |
      | Invalid parameter value: (.*). Supported values are: non-existing-class |

    Examples: 
      | old_class_index | class_index | exceptionText_index |
      | 0               | 0           | 0                   |
      | 0               | 1           | 0                   |
      
      