# -*- coding: utf-8 -*-
Feature: Class Modification
  
  As a class provider I would like to change the basic information associated to the class

  @method_not_allowed
  Scenario Outline: Class update with wrong method
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0            |
    When I try to put in $base_api_url/$classes_url/$class_name the class data <class_index>:
      | class_name | description   | default_version |
      | Class      | Class_updated | v1.0            |
    Then I get an error response of type 405 with error code SVC1003
    And the exceptionText contains <exceptionText_index>
      | exceptionText                           |
      | Requested Operation does not exist:(.*) |

    Examples: 
      | old_class_index | class_index | exceptionText_index |
      | 0               | 0           | 0                   |

  @internal_error
  Scenario Outline: Modification of a class when the DB is down_TDAFBA-463
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0            |
    And the DB has stopped working
    When I send to $base_api_url/$classes_url/$class_name the class data <class_index>:
      | description      | default_version |
      | Some description | v1.0            |
    Then I get an error response of type 500 with error code SVR1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText            |
      | Generic Server Error(.*) |

    Examples: 
      | old_class_index | class_index | exceptionText_index |
      | 0               | 0           | 0                   |

  @resource_not_found
  Scenario Outline: Modification of a class not already published_TDAFBA-461
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has not already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I send to $base_api_url/$classes_url/$class_name the class data <class_index>:
      | description      | default_version |
      | Some description | v1.0            |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | class_index | exceptionText_index |
      | 0               | 0           | 0                   |

  @malformed_request
  Scenario Outline: Publication of a new class using unstructured data_TDAFBA-467
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0            |
    When I send to $base_api_url/$classes_url/$class_name the data UNSTRUCTURED_DATA
    Then I get an error response of type 403 with error code POL0011
    And the exceptionText contains <exceptionText_index>:
      | exceptionText                                |
      | Media type (.*) not supported |

    Examples: 
      | exceptionText_index | old_class_index |
      | 0                   | 0               |

  @malformed_request
  Scenario Outline: Publication of a new class using malformed data
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0            |
    When I send to $base_api_url/$classes_url/$class_name the data MALFORMED_DATA
    Then I get an error response of type 400 with error code SVC1023
    And the exceptionText contains <exceptionText_index>
      | exceptionText                              |
      | Parser Error: (.*) content not well formed |

    Examples: 
      | exceptionText_index | old_class_index |
      | 0                   | 0               |

  @parameters_validation
  Scenario Outline: Modification of a class with invalid data_TDAFBA-458
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class0     | Class       | v1.0            |
      | Class1     | Class       | v1.0            |
      | Class2     | Class       | v1.0            |
      | Class3     | Class       | v1.0            |
      | Class4     | Class       | v1.0            |
      | Class5     | Class       | v1.0            |
    When I send to $base_api_url/$classes_url/$class_name the class data <class_index>:
      | description                 | default_version                 |
      |                             |                                 |
      | Some description            |                                 |
      | [STRING_WITH_LENGTH_1025]   | over_boundary_value_description |
      | over_boundary_value_version | [STRING_WITH_LENGTH_257]        |
      | 1.0                         | Non_string_description          |
      | Non_string_default_version  | 1.0                             |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                 |
      | Invalid parameter value: (.*) |

    Examples: 
      | old_class_index | class_index | exceptionText_index |
      | 0               | 0           | 0                   |
      | 1               | 1           | 0                   |
      | 2               | 2           | 0                   |
      | 3               | 3           | 0                   |
      | 4               | 4           | 0                   |
      | 5               | 5           | 0                   |

  @parameter_validation
  Scenario Outline: Modification of a class changing class_name to uppercase_TDAFBA-462
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | class      | Class       | v1.0            |
    When I send to $base_api_url/$classes_url/CLASS the class data <class_index>:
      | description      | default_version |
      | Some description | v1.0            |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | class_index | exceptionText_index |
      | 0               | 0           | 0                   |

  @happy_path
  Scenario Outline: Modification of a class with valid mandatory data_TDAFBA-455
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class0     | Class       | v1.0            |
      | Class1     | Class       | v1.0            |
      | Class2     | Class       | v1.0            |
      | Class3     | Class       | v1.0            |
      | Class4     | Class       | v1.0            |
      | Class5     | Class       | v1.0            |
    When I send to $base_api_url/$classes_url/$class_name the class data <class_index>:
      | default_version          |
      | v                        |
      | v1.0                     |
      | v57.12.12.110b-unstable  |
      | á.é.í                    |
      | [STRING_WITH_LENGTH_255] |
      | [STRING_WITH_LENGTH_256] |
    Then I get a success response of type 200 with the updated class data
    And the URL $base_api_url/$classes_url/$class_name returns the updated class data

    Examples: 
      | old_class_index | class_index |
      | 0               | 0           |
      | 1               | 1           |
      | 2               | 2           |
      | 3               | 3           |
      | 4               | 4           |
      | 5               | 5           |

  @happy_path
  Scenario Outline: Modification of a class with valid mandatory and optional data_TDAFBA-456
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class0     | Class       | v1.0            |
      | Class1     | Class       | v1.0            |
      | Class2     | Class       | v1.0            |
      | Class3     | Class       | v1.0            |
      | Class4     | Class       | v1.0            |
      | Class5     | Class       | v1.0            |
      | Class6     | Class       | v1.0            |
      | Class7     | Class       | v1.0            |
    When I send to $base_api_url/$classes_url/$class_name the class data <class_index>:
      | description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | default_version                  |
      | d                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | v                                |
      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | v1.0                              |
      | Short Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | v1.0                              |
      | Long description which contains a small story in several lines.\nEvery Sunday, the birds go to their bird church. All the birds in that parish go there. Starlings, eagles, pigeons, sparrows, blackbirds, ducks, geese, and so on.\nThe birds enter the church. Gravely, silently, they file into the church and find their way to their seats in the wooden church pews.\nMusic plays. Then, the bird preacher enters the room, using a small door behind the main altar. The bird preacher makes a dramatic gesture. Then he clears his throat and addresses his congregation. | v1.0                              |
      | Description with symbols: _-+*=.,;"'@#$%()/\\?!                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | v1.0                              |
      | ñçüúóíéá                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | v1.0                              |
      | [STRING_WITH_LENGTH_1023]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | under_boundary_value_description |
      | [STRING_WITH_LENGTH_1024]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | boundary_value_description       |
    Then I get a success response of type 200 with the updated class data
    And the URL $base_api_url/$classes_url/$class_name returns the updated class data

    Examples: 
      | old_class_index | class_index |
      | 0               | 0           |
      | 1               | 1           |
      | 2               | 2           |
      | 3               | 3           |
      | 4               | 4           |
      | 5               | 5           |
      | 6               | 6           |
      | 7               | 7           |

  @optional_data
  Scenario Outline: Modification of a class adding just optional data that was not there_TDAFBA-457
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | default_version |
      | Class      | v1.0            |
    When I send to $base_api_url/$classes_url/$class_name the class data <class_index>:
      | description      |
      | Some description |
    Then I get a success response of type 200 with the updated class data
    And the URL $base_api_url/$classes_url/$class_name returns the updated class data

    Examples: 
      | old_class_index | class_index |
      | 0               | 0           |

  @ignored_param
  Scenario Outline: Modification of a class with a new class_name which is ignored_TDAFBA-460
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0            |
    When I send to $base_api_url/$classes_url/$class_name the class data <class_index>:
      | class_name | description      | default_version |
      | Name       | Some description | v1.0            |
    # the new class_name is sent to the server, but not considered in the following steps
    Then I get a success response of type 200 with the updated class data

    Examples: 
      | old_class_index | class_index |
      | 0               | 0           |
