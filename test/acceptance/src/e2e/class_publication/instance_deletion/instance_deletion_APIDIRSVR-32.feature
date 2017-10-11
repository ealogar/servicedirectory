# -*- coding: utf-8 -*-
Feature: Endpoint Deleting
  
  As a class provider
  I would like to can to delete an instance
  to stop exposing an class in that instace

  @happy_path
  Scenario Outline: Deletion of an instance with mandatory data_TDAFBA-532
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0     | http://instance.tid.es |
    When I delete $base_api_url/$classes_url/$class_name/$instances_url/$instance_id
    Then I get a success response of type 204
    And the URL $base_api_url/$classes_url/$class_name/$instances_url/$instance_id returns the error code 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | exceptionText_index |
      | 0               | 0                  | 0                   |

  @happy_path
  Scenario Outline: Deletion of an instance with mandatory and optional data_TDAFBA-533
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                     | environment | attributes_keys  | attributes_values |
      | v1.0     | http://instance1.tid.es | test           | keytrue,keyfalse | True,False        |
    When I delete $base_api_url/$classes_url/$class_name/$instances_url/$instance_id
    Then I get a success response of type 204
    And the URL $base_api_url/$classes_url/$class_name/$instances_url/$instance_id returns the error code 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | exceptionText_index |
      | 0               | 0                  | 0                   |

  @method_not_allowed
  Scenario Outline: Deletion the instance collections
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I delete $base_api_url/$classes_url/$class_name/$instances_url
    Then I get an error response of type 405 with error code SVC1003
    And the exceptionText contains <exceptionText_index>
      | exceptionText                           |
      | Requested Operation does not exist:(.*) |

    Examples: 
      | old_class_index | exceptionText_index |
      | 0               | 0                   |

  @resource_not_found
  Scenario Outline: Deletion of an instance over an non existing class and non existing instance
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I delete $base_api_url/$classes_url/Non_existing_Class/$instances_url/5209008cfe813b1858611c3d
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | exceptionText_index |
      | 0               | 0                   |

  @resource_not_found
  Scenario Outline: Deletion of an instance over an non existing class and existing instance
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0     | http://instance.tid.es |
    When I delete $base_api_url/$classes_url/Non_existing_Class/$instances_url/$instance_id
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | exceptionText_index |
      | 0               | 0                  | 0                   |

  @resource_not_found
  Scenario Outline: Deletion of an instance not already published_TDAFBA-534
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has not already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0     | http://instance.tid.es |
    When I delete $base_api_url/$classes_url/$class_name/$instances_url/$instance_id
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | exceptionText_index |
      | 0               | 0                  | 0                   |

  @resource_not_found
  Scenario Outline: Deletion of an existing instance and existing class but not related
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0     | http://instance.tid.es |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class2     | Class       | v1.0             |
    When I delete $base_api_url/$classes_url/$class_name/$instances_url/$instance_id
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Invalid parameter value: (.*). Supported values are: (.*) |

    Examples: 
      | old_class_index | old_instance_index | exceptionText_index |
      | 0               | 0                  | 0                   |

  @internal_error
  Scenario Outline: Deletion of an instance when the DB is down_TDAFBA-535
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v1.0     | http://instance.tid.es | integration |
    And the DB has stopped working
    When I delete $base_api_url/$classes_url/$class_name/$instances_url/$instance_id
    Then I get an error response of type 500 with error code SVR1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText            |
      | Generic Server Error(.*) |

    Examples: 
      | old_class_index | old_instance_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0              | 0                   |
