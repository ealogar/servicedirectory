# -*- coding: utf-8 -*-
Feature: Instance Discovering
  
  As a SD manager 
  I want users access to be controlled
  so that they can only perform operations granted for them

  Scenario Outline: Perform operations without the authentication header
    Given no users are previously created in the system
    And no authentication method is provided
    When I send to $base_api_url/$classes_url the class data <class_index>:
      | class_name | default_version |
      | Class0       | v1.0               |
    Then I get an error response of type 403 with error code SVC1019
    And the exceptionText contains <exceptionText_index>
      | exceptionText                      |
      | Application cannot use API/Feature |

    Examples: 
      | class_index | exceptionText_index |
      | 0         | 0                   |

  Scenario Outline: Perform request with wrong credentials (non_existing, wrong_pass and empty user)
    Given no users are previously created in the system
    And the user performing the operation is <creation_user_index>:
      | username | password |
      | admin    | admin    |
    And a user has already been created with data <user_data_index>:
      | username   | password      |
      | user_test1 | password_test |
    And the user performing the operation is <user_index>:
      | username     | password   |
      | user_test1   | other_pass |
      | non_existing | other_pass |
      |              | empty_user |
    When I send to $base_api_url/$classes_url the class data <class_index>:
      | class_name | default_version |
      | Class0       | v1.0               |
    Then I get an error response of type 401 with error code SVC1018
    And the exceptionText contains <exceptionText_index>
      | exceptionText       |
      | Invalid Credentials |

    Examples: 
      | creation_user_index | user_data_index | user_index | class_index | exceptionText_index |
      | 0                   | 0               | 0          | 0         | 0                   |
      | 0                   | 0               | 1          | 0         | 0                   |
      | 0                   | 0               | 2          | 0         | 0                   |

  Scenario Outline: Creation of Classs without admin privileges
    Given no users are previously created in the system
    And the user performing the operation is <creation_user_index>:
      | username | password |
      | admin    | admin    |
    And a user has already been created with data <user_data_index>:
      | username   | password      |
      | user_test1 | password_test |
    And the user performing the operation is <user_index>:
      | username   | password      |
      | user_test1 | password_test |
    When I send to $base_api_url/$classes_url the class data <class_index>:
      | class_name | default_version |
      | Class0       | v1.0               |
    Then I get an error response of type 403 with error code SVC1013
    And the exceptionText contains <exceptionText_index>
      | exceptionText                      |
      | (.*) Operation is not allowed:(.*) |

    Examples: 
      | creation_user_index | user_data_index | user_index | class_index | exceptionText_index |
      | 0                   | 0               | 0          | 0         | 0                   |

  Scenario Outline: Creation of Classs with admin privileges
    Given the DB has no classes already published
    And no users are previously created in the system
    And the user performing the operation is <creation_user_index>:
      | username | password |
      | admin    | admin    |
    And a user has already been created with data <user_data_index>:
      | username    | password    | is_admin |
      | other_admin | other_admin | [TRUE]     |
    And the user performing the operation is <operation_user_index>:
      | username    | password    |
      | admin       | admin       |
      | other_admin | other_admin |
    When I send to $base_api_url/$classes_url the class data <class_index>:
      | class_name | default_version |
      | Class0       | v1.0               |
      | Class1       | v1.0               |
    Then I get a success response of type 201

    Examples: 
      | creation_user_index | user_data_index | creation_user_index | operation_user_index | class_index |
      | 0                   | 0               | 0                   | 0                    | 0         |
      | 0                   | 0               | 0                   | 1                    | 1         |

  Scenario Outline: Creation instance without privileges
    Given no users are previously created in the system
    And the user performing the operation is <creation_user_index>:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class1       | Class  | v1.0             |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class2       | Class  | v1.0             |
    And a user has already been created with data <user_data_index>:
      | username   | password      | is_admin | classes |
      | user_test1 | password_test | [FALSE]    |         |
      | user_test2 | password_test | [FALSE]    | Class2    |
    And the user performing the operation is <operation_user_index>:
      | username   | password      |
      | user_test1 | password_test |
      | user_test2 | password_test |
    When I send to $base_api_url/$classes_url/Class1/$instances_url the instance data <instance_index>:
      | version | uri      |
      | v1      | fake_url |
    Then I get an error response of type 403 with error code SVC1013
    And the exceptionText contains <exceptionText_index>
      | exceptionText                      |
      | (.*) Operation is not allowed:(.*) |

    Examples: 
      | user_data_index | creation_user_index | operation_user_index | old_class_index | instance_index | exceptionText_index |
      | 0               | 0                   | 0                    | 0             | 0              | 0                   |
      | 1               | 0                   | 1                    | 0             | 0              | 0                   |

  Scenario Outline: Creation instance with privileges
    Given no users are previously created in the system
    And the user performing the operation is <creation_user_index>:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And a user has already been created with data <user_data_index>:
      | username   | password      | is_admin | classes |
      | user_test1 | password_test |  [TRUE]     |         |
      | user_test2 | password_test | [FALSE]    | Class     |
    And the user performing the operation is <operation_user_index>:
      | username   | password      |
      | admin      | admin         |
      | user_test1 | password_test |
      | user_test2 | password_test |
    When I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri      |
      | v1      | fake_url |
    Then I get a success response of type 201

    Examples: 
      | user_data_index | creation_user_index | operation_user_index | old_class_index | instance_index |
      | 0               | 0                   | 0                    | 0             | 0              |
      | 0               | 0                   | 1                    | 0             | 0              |
      | 1               | 0                   | 2                    | 0             | 0              |

  Scenario Outline: Creation of bindings with privileges
    Given no users are previously created in the system
    And the user performing the operation is <creation_user_index>:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And a user has already been created with data <user_data_index>:
      | username   | password      | is_admin | classes | origins           |
      | user_test1 | password_test |  [TRUE]     |         |                   |
      | user_test2 | password_test | [FALSE]    | Class     |                   |
      | user_test3 | password_test | [FALSE]    | Class     | Apiname0          |
      | user_test4 | password_test | [FALSE]   |         | Apiname0          |
      | user_test5 | password_test | [FALSE]    |         | Apiname0,Apiname1 |
    And the user performing the operation is <operation_user_index>:
      | username   | password      |
      | admin      | admin         |
      | user_test1 | password_test |
      | user_test2 | password_test |
      | user_test3 | password_test |
      | user_test4 | password_test |
      | user_test5 | password_test |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And the following bindings rules are available <operation_rule_index>:
      | operation | input_context_param | value |
      | eq        | rule                | 1     |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin   | class_name |
      | Apiname0 | Class        |
      | default  | Class        |
    Then I get a success response of type 201

    Examples: 
      | user_data_index | creation_user_index | operation_user_index | old_instance_index|operation_index | old_class_index | binding_index |
      | 0               | 0                   | 0                    | 0  |0  | 0           | 0             |
      | 0               | 0                   | 1                    | 0  |0  | 0           | 1             |
      | 0               | 0                   | 1                    | 0  |0  | 0           | 0             |
      | 0               | 0                   | 1                    | 0  |0  | 0           | 1             |
      | 1               | 0                   | 2                    | 0  |0  | 0           | 1             |
      | 2               | 0                   | 3                    |0  | 0  | 0           | 0             |
      | 2               | 0                   | 3                    | 0  |0  | 0           | 1             |
 #     | 3               | 0                   | 4                    | 0  |0  | 0           | 0             |
 #     | 4               | 0                   | 5                    | 0  |0  | 0           | 0             |

  Scenario Outline: Creation of bindings without privileges
    Given no users are previously created in the system
    And the user performing the operation is <creation_user_index>:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And a user has already been created with data <user_data_index>:
      | username   | password      | is_admin | classes | origins  |
      | user_test1 | password_test | [FALSE]    |         |          |
      | user_test2 | password_test | [FALSE]   | Class     |          |
      | user_test3 | password_test | [FALSE]    | Class     | Apiname1 |
      | user_test4 | password_test | [FALSE]    |         | Apiname0 |
    And the user performing the operation is <operation_user_index>:
      | username   | password      |
      | user_test1 | password_test |
      | user_test2 | password_test |
      | user_test3 | password_test |
      | user_test4 | password_test |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | eq        | rule                | 1     |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin   | class_name |
      | Apiname0 | Class        |
      | default  | Class        |
    Then I get an error response of type 403 with error code SVC1013
    And the exceptionText contains <exceptionText_index>
      | exceptionText                      |
      | (.*) Operation is not allowed:(.*) |

    Examples: 
      | user_data_index | creation_user_index | operation_user_index | old_class_index | binding_index | exceptionText_index |
      | 0               | 0                   | 0                    | 0             | 0             | 0                   |
      | 0               | 0                   | 0                    | 0             | 1             | 0                   |
      | 1               | 0                   | 1                    | 0             | 0             | 0                   |
      | 2               | 0                   | 2                    | 0             | 0             | 0                   |
      | 3               | 0                   | 3                    | 0             | 1             | 0                   |

  Scenario Outline: Deleting resources with privileges
    Given no users are previously created in the system
    And the user performing the operation is <creation_user_index>:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And a user has already been created with data <user_data_index>:
      | username   | password      | is_admin | classes | origins           |
      | user_test1 | password_test |  [TRUE]     |         |                   |
      | user_test2 | password_test | [FALSE]    | Class     |                   |
      | user_test3 | password_test | [FALSE]    | Class     | Apiname0          |
      | user_test4 | password_test | [FALSE]    |         | Apiname0          |
      | user_test5 | password_test | [FALSE]    |         | Apiname0,Apiname1 |
    And the user performing the operation is <operation_user_index>:
      | username   | password      |
      | admin      | admin         |
      | user_test1 | password_test |
      | user_test2 | password_test |
      | user_test3 | password_test |
      | user_test4 | password_test |
      | user_test5 | password_test |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | eq        | rule                | 1     |
    When I send to $base_api_url/$bindings_url the rule data <binding_index>:
      | origin   | class_name |
      | Apiname0 | Class        |
      | default  | Class        |
    And I delete resource <resource_index>:
      | resource                                                      |
      | $base_api_url/$classes_url/Class                                   |
      | $base_api_url/$classes_url/$class_name/$instances_url/$instance_id |
      | $base_api_url/$bindings_url/$binding_id                       |
      | $base_api_url/$bindings_url/$binding_id                       |
    Then I get a success response of type 204

    Examples: 
      | creation_user_index | old_class_index | old_instance_index | user_data_index | operation_user_index | operation_index | binding_index | resource_index |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 0             | 0              |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 0             | 1              |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 0             | 2              |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 1             | 3              |
      | 0                   | 0             | 0                  | 0               | 1                    | 0               | 0             | 0              |
      | 0                   | 0             | 0                  | 0               | 1                    | 0               | 0             | 1              |
      | 0                   | 0             | 0                  | 0               | 1                    | 0               | 0             | 2              |
      | 0                   | 0             | 0                  | 0               | 1                    | 0               | 1             | 3              |
      | 0                   | 0             | 0                  | 1               | 2                    | 0               | 0             | 0              |
      | 0                   | 0             | 0                  | 1               | 2                    | 0               | 0             | 1              |
      | 0                   | 0             | 0                  | 1               | 2                    | 0               | 1             | 3              |
      | 0                   | 0             | 0                  | 2               | 3                    | 0               | 0             | 0              |
      | 0                   | 0             | 0                  | 2               | 3                    | 0               | 0             | 1              |
      | 0                   | 0             | 0                  | 2               | 3                    | 0               | 0             | 2              |
      | 0                   | 0             | 0                  | 2               | 3                    | 0               | 1             | 3              |
      | 0                   | 0             | 0                  | 3               | 4                    | 0               | 0             | 2              |
      | 0                   | 0             | 0                  | 4               | 5                    | 0               | 0             | 2              |

  @bug
  Scenario Outline: Deleting without privileges
    Given no users are previously created in the system
    And the user performing the operation is <creation_user_index>:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And a user has already been created with data <user_data_index>:
      | username   | password      | is_admin | classes | origins  |
      | user_test1 | password_test | [FALSE]    | Class     |          |
      | user_test2 | password_test | [FALSE]    |         | Apiname0 |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | eq        | rule                | 1     |
    And the previous bindings are published for the context <context_index>:
      | origin   | class_name |
      | default  | Class        |
      | Apiname0 | Class        |
    Given the user performing the operation is <operation_user_2_index>:
      | username   | password      |
      | user_test1 | password_test |
      | user_test2 | password_test |
    When I delete resource <resource_index>:
      | resource                                                      |
      | $base_api_url/$classes_url/Class                                   |
      | $base_api_url/$classes_url/$class_name/$instances_url/$instance_id |
      | $base_api_url/$bindings_url/$binding_id                       |
    Then I get an error response of type 403 with error code SVC1013
    And the exceptionText contains <exceptionText_index>
      | exceptionText                      |
      | (.*) Operation is not allowed:(.*) |

    Examples: 
      | creation_user_index | old_class_index | old_instance_index | user_data_index | operation_user_2_index | operation_index | context_index | resource_index | exceptionText_index |
  #    | 0                   | 0             | 0                  | 0               | 0                      | 0               | 0             | 2              | 0                   |
      | 0                   | 0             | 0                  | 1               | 1                      | 0               | 1             | 0              | 0                   |
      | 0                   | 0             | 0                  | 1               | 1                      | 0               | 1             | 1              | 0                   |
      | 0                   | 0             | 0                  | 1               | 1                      | 0               | 0             | 2              | 0                   |


  Scenario Outline: Getting information from resources with privileges
    Given no users are previously created in the system
    And the user performing the operation is <creation_user_index>:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And a user has already been created with data <user_data_index>:
      | username   | password      | is_admin | classes | origins           |
      | user_test1 | password_test |  [TRUE]     |         |                   |
      | user_test2 | password_test | [FALSE]    | Class     |                   |
      | user_test3 | password_test | [FALSE]    | Class     | Apiname0          |
      | user_test4 | password_test | [FALSE]    |         | Apiname0          |
      | user_test5 | password_test | [FALSE]   |         | Apiname0,Apiname1 |
    And the user performing the operation is <operation_user_index>:
      | username   | password      |
      | admin      | admin         |
      | user_test1 | password_test |
      | user_test2 | password_test |
      | user_test3 | password_test |
      | user_test4 | password_test |
      | user_test5 | password_test |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | eq        | rule                | 1     |
    And the previous bindings are published for the context <context_index>:
      | origin   | class_name |
      | Apiname0 | Class        |
      | default  | Class        |
    When I check the resource <resource_index>:
      | resource                                                      |
      | $base_api_url/$classes_url/Class                                   |
      | $base_api_url/$classes_url/$class_name/$instances_url/$instance_id |
      | $base_api_url/$bindings_url/$binding_id                       |
      | $base_api_url/$users_url                                      |
      | $base_api_url/$users_url/admin                                |
    Then I get a success response of type 200

    Examples: 
      | creation_user_index | old_class_index | old_instance_index | user_data_index | operation_user_index | operation_index | context_index | resource_index |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 0             | 0              |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 0             | 1              |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 0             | 2              |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 1             | 2              |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 0             | 3              |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 0             | 3              |
      | 0                   | 0             | 0                  | 0               | 1                    | 0               | 0             | 0              |
      | 0                   | 0             | 0                  | 0               | 1                    | 0               | 0             | 1              |
      | 0                   | 0             | 0                  | 0               | 1                    | 0               | 0             | 2              |
      | 0                   | 0             | 0                  | 0               | 1                    | 0               | 1             | 2              |
      | 0                   | 0             | 0                  | 1               | 2                    | 0               | 0             | 0              |
      | 0                   | 0             | 0                  | 1               | 2                    | 0               | 0             | 1              |
      | 0                   | 0             | 0                  | 1               | 2                    | 0               | 1             | 2              |
      | 0                   | 0             | 0                  | 2               | 3                    | 0               | 0             | 0              |
      | 0                   | 0             | 0                  | 2               | 3                    | 0               | 0             | 1              |
      | 0                   | 0             | 0                  | 2               | 3                    | 0               | 0             | 2              |
      | 0                   | 0             | 0                  | 2               | 3                    | 0               | 1             | 2              |
      | 0                   | 0             | 0                  | 3               | 4                    | 0               | 0             | 0              |
      | 0                   | 0             | 0                  | 3               | 4                    | 0               | 0             | 1              |
      | 0                   | 0             | 0                  | 3               | 4                    | 0               | 0             | 2              |
      | 0                   | 0             | 0                  | 4               | 5                    | 0               | 0             | 0              |
      | 0                   | 0             | 0                  | 4               | 5                    | 0               | 0             | 1              |
      | 0                   | 0             | 0                  | 4               | 5                    | 0               | 0             | 2              |

  # All users can access to all resoruces, with our without privileges
  Scenario Outline: Getting information from resources without privileges
    Given no users are previously created in the system
    And the user performing the operation is <creation_user_index>:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class        | Class  | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And a user has already been created with data <user_data_index>:
      | username   | password      | is_admin | classes | origins  |
      | user_test1 | password_test | [FALSE]    | Class     |          |
      | user_test2 | password_test | [FALSE]    |         | Apiname0 |
    And the user performing the operation is <operation_user_index>:
      | username   | password      |
      | user_test1 | password_test |
      | user_test2 | password_test |
    And the following bindings rules are available <operation_index>:
      | operation | input_context_param | value |
      | eq        | rule                | 1     |
    And the previous bindings are published for the context <context_index>:
      | origin   | class_name |
      | default | Class        |
      | Apiname0  | Class        |
    When I check the resource <resource_index>:
      | resource                                                      |
      | $base_api_url/$classes_url/Class                                   |
      | $base_api_url/$classes_url/$class_name/$instances_url/$instance_id |
      | $base_api_url/$bindings_url/$binding_id                       |
    Then I get a success response of type 200

    Examples: 
      | creation_user_index | old_class_index | old_instance_index | user_data_index | operation_user_index | operation_index | context_index | resource_index | exceptionText_index |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 0             | 0              | 0                   |
      | 0                   | 0             | 0                  | 1               | 1                    | 0               | 1             | 0              | 0                   |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 0             | 1              | 0                   |
      | 0                   | 0             | 0                  | 1               | 1                    | 0               | 1             | 1              | 0                   |
      | 0                   | 0             | 0                  | 0               | 0                    | 0               | 0             | 2              | 0                   |
      | 0                   | 0             | 0                  | 1               | 1                    | 0               | 1             | 2              | 0                   |

  #only admin users can access to users resources
  Scenario Outline: Getting information from resources without privileges (user resource)
    Given no users are previously created in the system
    And the user performing the operation is <creation_user_index>:
      | username | password |
      | admin    | admin    |
    And a user has already been created with data <user_data_index>:
      | username   | password      | is_admin |
      | user_test1 | password_test | [FALSE]    |
    And the user performing the operation is <operation_user_index>:
      | username   | password      |
      | user_test1 | password_test |
    When I check the resource <resource_index>:
      | resource                       |
      | $base_api_url/$users_url/      |
      | $base_api_url/$users_url/admin |
    Then I get an error response of type 403 with error code SVC1013
    And the exceptionText contains <exceptionText_index>
      | exceptionText                      |
      | (.*) Operation is not allowed:(.*) |

    Examples: 
      | creation_user_index | user_data_index | operation_user_index | resource_index | exceptionText_index |
      | 0                   | 0               | 0                    | 0              | 0                   |
      | 0                   | 0               | 0                    | 1              | 0                   |
