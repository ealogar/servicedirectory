# -*- coding: utf-8 -*-
Feature: User creation
  
  As a admin role 
  I want to create, update and delete users
  so that they can manages the instances and rules of the classes

  Scenario Outline: User basic creation
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$users_url the user data <user_data_index>:
      | username                                                                    | password                                                                        |
      | user_test                                                                   | password_test                                                                   |
      | user_test                                                                   | Strange pass with chars#ñ.! & spaces                                            |
      | VaLid_user-name                                                             | password_test                                                                   |
      | Looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong_user | password_test                                                                   |
      | user_test                                                                   | Looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong_password |
    Then I get a success response of type 201 with location <location_index>:
      | location                                                                                             |
      | $base_api_url/$users_url/user_test                                                                   |
      | $base_api_url/$users_url/user_test                                                                   |
      | $base_api_url/$users_url/VaLid_user-name                                                             |
      | $base_api_url/$users_url/Looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong_user |
      | $base_api_url/$users_url/user_test                                                                   |
    And the response contains the user data
    And the location returns the user data

    Examples: 
      | user_index | user_data_index | location_index |
      | 0          | 0               | 0              |
      | 0          | 1               | 1              |
      | 0          | 2               | 2              |
      | 0          | 3               | 3              |
      | 0          | 4               | 4              |

  Scenario Outline: User creation with non existing user
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username   | password      |
      | user_test1 | password_test |
    When I send to $base_api_url/$users_url the user data <user_data_index>:
      | username   | password       |
      | user_test2 | password_test2 |
    Then I get an error response of type 401 with error code SVC1018
    And the exceptionText contains <exceptionText_index>
      | exceptionText       |
      | Invalid Credentials |

    Examples: 
      | user_index | user_data_index | location_index | exceptionText_index |
      | 0          | 0               | 0              | 0                   |

  Scenario Outline: User creation without rigths
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    Given a user has already been created with data <user_data_index>:
      | username   | password      |
      | user_test1 | password_test |
    Given the user performing the operation is <user_index>:
      | username   | password      |
      | user_test1 | password_test |
    When I send to $base_api_url/$users_url the user data <user_data_index>:
      | username   | password      |
      | user_test2 | password_test |
    Then I get an error response of type 403 with error code SVC1013
    And the exceptionText contains <exceptionText_index>
      | exceptionText                      |
      | (.*) Operation is not allowed:(.*) |

    Examples: 
      | user_index | user_data_index | location_index | exceptionText_index |
      | 0          | 0               | 0              | 0                   |

  Scenario Outline: User creation with missing mandatory params
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$users_url the user data <user_data_index>:
      | username        | password        |
      | [MISSING_PARAM] | password_test   |
      | user_test       | [MISSING_PARAM] |
    Then I get an error response of type 400 with error code SVC1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText                    |
      | Missing mandatory parameter:(.*) |

    Examples: 
      | user_index | user_data_index | location_index | exceptionText_index |
      | 0          | 0               | 0              | 0                   |
      | 0          | 1               | 0              | 0                   |

  Scenario Outline: Non valid user or password in user creation
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$users_url the user data <user_data_index>:
      | username         | password      |
      | user_#test       | password_test |
      |                  | password_test |
      | user_#test       |               |
      | Nón_ascii        | password_test |
      | user with spaces | password_test |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                 |
      | Invalid parameter value: (.*) |

    Examples: 
      | user_index | user_data_index | location_index | exceptionText_index |
      | 0          | 0               | 0              | 0                   |
      | 0          | 1               | 0              | 0                   |
      | 0          | 2               | 0              | 0                   |
      | 0          | 3               | 0              | 0                   |
      | 0          | 4               | 0              | 0                   |

  Scenario Outline: Existing username
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    When I send to $base_api_url/$users_url the user data <user_data_index>:
      | username | password |
      | admin    | admin    |
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                                          |
      | Invalid parameter value: (.*). Supported values are: non-existing-user |

    Examples: 
      | user_index | user_data_index | location_index | exceptionText_index |
      | 0          | 0               | 0              | 0                   |

  Scenario Outline: Valid extra parameters in user creation
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class1       | Class  | v1.0             |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class2       | Class  | v1.0             |
    When I send to $base_api_url/$users_url the user data <user_data_index>:
      | username  | password      | is_admin | classes   | origins |
      | user_test | password_test | [TRUE]     | Class1,Class2 | Or1,Or2 |
      | user_test | password_test | [FALSE]   | Class1,Class2 | Or1,Or2 |
      | user_test | password_test | [FALSE]    |           |         |
    Then I get a success response of type 201 with location <location_index>:
      | location                           |
      | $base_api_url/$users_url/user_test |
      | $base_api_url/$users_url/user_test |
      | $base_api_url/$users_url/user_test |
    And the response contains the user data
    And the location returns the user data

    Examples: 
      | old_class_index | user_index | user_data_index | location_index |
      | 0             | 0          | 0               | 0              |
      | 0             | 0          | 1               | 1              |
      | 0             | 0          | 2               | 2              |

  @bug(APIDIRSVR-549,APIDIRSVR-550)
  Scenario Outline: Non valid extra parameters in user creation (non_existing)
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class0       | Class  | v1.0             |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class1       | Class  | v1.0             |
    When I send to $base_api_url/$users_url the user data <user_data_index>:
      | username  | password      | is_admin | classes     | origins |
      | user_test | password_test | [TRUE]      | Class1,Class3   | Or1,Or2 |
      | user_test | password_test | [FALSE]    | Class1,Class2   | Espana  |
      | user_test | password_test | False    | Class1,Class2   | Or1,Or2 |
      | user_test | password_test | 1    | Class1,Class2   | Or1,Or2 |
      | user_test | password_test |          | Class1,Class2   | Or1,Or2 |
      | user_test | password_test | [TRUE]      | Class1,Espana | Or1,Or2 |
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                           |
      | Invalid parameter value:(.*). Supported values are:(.*) |

    Examples: 
      | old_class_index | user_index | user_data_index | exceptionText_index |
      | 0             | 0          | 0               | 0                   |
      | 0             | 0          | 1               | 0                   |
      | 0             | 0          | 2               | 0                   |
      | 0             | 0          | 3               | 0                   |
      | 0             | 0          | 4               | 0                   |
      | 0             | 0          | 5               | 0                   |
      
    Scenario Outline: Non valid extra parameters in user creation (characters invalid)
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class0       | Class  | v1.0             |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class1       | Class  | v1.0             |
    When I send to $base_api_url/$users_url the user data <user_data_index>:
      | username  | password      | is_admin | classes     | origins |
      | user_test | password_test | [FALSE]    | Class1,Class0   | España  |
      | user_test | password_test | [TRUE]     | Class1,España | Or1,Or2 |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Invalid parameter value:(.*) |

    Examples: 
      | old_class_index | user_index | user_data_index | exceptionText_index |
      | 0             | 0          | 0               | 0                   |
      | 0             | 0          | 1               | 0                   |


  Scenario Outline: Deletion of an user with admin
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class1       | Class  | v1.0             |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class2       | Class  | v1.0             |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class3       | Class  | v1.0             |
    Given a user has already been created with data <user_data_index>:
      | username  | password      | is_admin        | classes         | origins         |
      | user_test | password_test | [TRUE]             | Class1,Class3       | Or1,Or2         |
      | user_test | password_test | [FALSE]           | Class1,Class2       | Or1,Or2         |
      | user_test | password_test | [MISSING_PARAM] | [MISSING_PARAM] | [MISSING_PARAM] |
      | user_test | password_test | [TRUE]             |                 |                 |
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    When I delete $base_api_url/$users_url/user_test
    Then I get a success response of type 204
    And the URL $base_api_url/$users_url/user_test returns the error code 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | user_data_index | user_index | exceptionText_index | old_class_index |
      | 0               | 0          | 0                   | 0             |
      | 1               | 0          | 0                   | 0             |
      | 2               | 0          | 0                   | 0             |
      | 3               | 0          | 0                   | 0             |

  Scenario Outline: Deletion of an user with non admin
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    Given a user has already been created with data <user_data_index>:
      | username   | password      |
      | user_test1 | password_test |
    Given a user has already been created with data <user_data_index>:
      | username   | password      |
      | user_test2 | password_test |
    Given the user performing the operation is <user_index>:
      | username   | password      |
      | user_test1 | password_test |
    When I delete $base_api_url/$users_url/user_test2
    Then I get an error response of type 403 with error code SVC1013
    And the exceptionText contains <exceptionText_index>
      | exceptionText                      |
      | (.*) Operation is not allowed:(.*) |

    Examples: 
      | user_data_index | user_index | exceptionText_index |
      | 0               | 0          | 0                   |

  Scenario Outline: Admin user trying to delete itself
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    Given a user has already been created with data <user_data_index>:
      | username      | password      | is_admin |
      | another_admin | another_admin | [TRUE]      |
    Given the user performing the operation is <user_index>:
      | username      | password      |
      | another_admin | another_admin |
    When I delete $base_api_url/$users_url/another_admin
    Then I get an error response of type 403 with error code SVC1013
    And the exceptionText contains <exceptionText_index>
      | exceptionText                      |
      | (.*) Operation is not allowed:(.*) |

    Examples: 
      | user_data_index | user_index | exceptionText_index |
      | 0               | 0          | 0                   |

  Scenario Outline: Default user deleting itself
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    When I delete $base_api_url/$users_url/admin
    Then I get an error response of type 403 with error code SVC1013
    And the exceptionText contains <exceptionText_index>
      | exceptionText                      |
      | (.*) Operation is not allowed:(.*) |

    Examples: 
      | user_data_index | user_index | exceptionText_index |
      | 0               | 0          | 0                   |

  Scenario Outline: Modification of an user with admin
    Given no users are previously created in the system
    Given the user performing the operation is <base_user_index>:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class1       | Class  | v1.0             |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class2       | Class  | v1.0             |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class3       | Class  | v1.0             |
    Given a user has already been created with data <old_user_data_index>:
      | username      | password      | is_admin |
      | another_admin | another_admin | [TRUE]      |
      | another_admin | another_admin | [TRUE]      |
      | another_admin | another_admin | [TRUE]      |
      | another_admin | another_admin | [TRUE]      |
    Given a user has already been created with data <old_user_data_index>:
      | username  | password      | is_admin        | classes         | origins         |
      | user_test | password_test | [TRUE]             | Class1,Class3       | Or1,Or2         |
      | user_test | password_test | [FALSE]           | Class1,Class2       | Or1,Or2         |
      | user_test | password_test | [MISSING_PARAM] | [MISSING_PARAM] | [MISSING_PARAM] |
      | user_test | password_test | [TRUE]             |                 |                 |
    Given the user performing the operation is <user_index>:
      | username      | password      |
      | admin         | admin         |
      | another_admin | another_admin |
    When I update $base_api_url/$users_url/ with the user data <user_data_index>:
      | username  | password      | is_admin | classes   | origins |
      | user_test | password_test | [FALSE]    | Class1,Class3 | Or1,Or2 |
      | user_test | password_test | [TRUE]      | Class1,Class2 | Or1,Or2 |
      | user_test | password_test | [TRUE]      |           |         |
    Then I get a success response of type 200
    And the response contains the user data

    Examples: 
      | old_user_data_index | user_index | user_data_index | base_user_index | old_class_index |
      | 0                   | 0          | 0               | 0               | 0             |
      | 0                   | 0          | 1               | 0               | 0             |
      | 0                   | 0          | 2               | 0               | 0             |
      | 1                   | 0          | 0               | 0               | 0             |
      | 1                   | 0          | 1               | 0               | 0             |
      | 1                   | 0          | 2               | 0               | 0             |
      | 2                   | 0          | 0               | 0               | 0             |
      | 2                   | 0          | 1               | 0               | 0             |
      | 2                   | 0          | 2               | 0               | 0             |
      | 3                   | 0          | 0               | 0               | 0             |
      | 3                   | 0          | 1               | 0               | 0             |
      | 3                   | 0          | 2               | 0               | 0             |
      | 0                   | 1          | 0               | 0               | 0             |
      | 0                   | 1          | 1               | 0               | 0             |
      | 0                   | 1          | 2               | 0               | 0             |
      | 1                   | 1          | 0               | 0               | 0             |
      | 1                   | 1          | 1               | 0               | 0             |
      | 1                   | 1          | 2               | 0               | 0             |
      | 2                   | 1          | 0               | 0               | 0             |
      | 2                   | 1          | 1               | 0               | 0             |
      | 2                   | 1          | 2               | 0               | 0             |
      | 3                   | 1          | 0               | 0               | 0             |
      | 3                   | 1          | 1               | 0               | 0             |
      | 3                   | 1          | 2               | 0               | 0             |

  Scenario Outline: Admin user trying to modify itself
    Given no users are previously created in the system
    Given the user performing the operation is <base_user_index>:
      | username | password |
      | admin    | admin    |
    Given a user has already been created with data <old_user_data_index>:
      | username      | password      | is_admin |
      | another_admin | another_admin | [TRUE]      |
    Given the user performing the operation is <user_index>:
      | username      | password      |
      | admin         | admin         |
      | another_admin | another_admin |
    When I update $base_api_url/$users_url/ with the user data <user_data_index>:
      | username      | password      | is_admin |
      | admin         | admin         | [FALSE]    |
      | another_admin | another_admin | [FALSE]    |
    Then I get an error response of type 403 with error code SVC1013
    And the exceptionText contains <exceptionText_index>
      | exceptionText                      |
      | (.*) Operation is not allowed:(.*) |

    Examples: 
      | base_user_index | old_user_data_index | user_index | user_data_index | exceptionText_index |
      | 0               | 0                   | 0          | 0               | 0                   |
      | 0               | 0                   | 1          | 1               | 0                   |

  Scenario Outline: Modifications of users without privileges
    Given no users are previously created in the system
    Given the user performing the operation is <user_index>:
      | username | password |
      | admin    | admin    |
    Given a user has already been created with data <user_data_index>:
      | username   | password      |
      | user_test1 | password_test |
    Given a user has already been created with data <user_data_index>:
      | username   | password      |
      | user_test2 | password_test |
    Given the user performing the operation is <user_index>:
      | username   | password      |
      | user_test1 | password_test |
    When I update $base_api_url/$users_url/ with the user data <user_data_index>:
      | username   | password       |
      | user_test2 | password_test2 |
    Then I get an error response of type 403 with error code SVC1013
    And the exceptionText contains <exceptionText_index>
      | exceptionText                      |
      | (.*) Operation is not allowed:(.*) |

    Examples: 
      | user_data_index | user_index | user_data_index | exceptionText_index |
      | 0               | 0          | 0               | 0                   |
