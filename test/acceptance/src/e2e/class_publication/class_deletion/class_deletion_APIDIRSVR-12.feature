# -*- coding: utf-8 -*-
Feature: Class Deleting
  
  As a class provider
  I would like to be able to delete a class exposed by the Service Directory
  so that I can remove non used classes

  @happy_path
  Scenario Outline: Deletion of a class with mandatory data_TDAFBA-527
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | default_version |
      | Class      | v1.0             |
    When I delete $base_api_url/$classes_url/$class_name
    Then I get a success response of type 204
    And the URL $base_api_url/$classes_url/$class_name returns the error code 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | exceptionText_index |
      | 0               | 0                   |

  @happy_path
  Scenario Outline: Deletion of a class with mandatory and optional data_TDAFBA-528
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I delete $base_api_url/$classes_url/$class_name
    Then I get a success response of type 204
    And the URL $base_api_url/$classes_url/$class_name returns the error code 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | exceptionText_index |
      | 0               | 0                   |

  @happy_path
  Scenario Outline: Deletion of a class with instances_TDAFBA-529
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v1.0     | http://instance.tid.es |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    |
      | v2.0     | http://instance.tid.es |
    When I delete $base_api_url/$classes_url/$class_name
    Then I get a success response of type 204
    And the URL $base_api_url/$classes_url/$class_name returns the error code 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | exceptionText_index |
      | 0               | 0                  | 0                   |

  @method_not_allowed
  Scenario Outline: Deletion the class collections
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    When I delete $base_api_url/$classes_url
    Then I get an error response of type 405 with error code SVC1003
    And the exceptionText contains <exceptionText_index>
      | exceptionText                           |
      | Requested Operation does not exist:(.*) |

    Examples: 
      | exceptionText_index |
      | 0                   |

  @resource_not_found
  Scenario Outline: Deletion of a class not already published_TDAFBA-530
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has not already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    When I delete $base_api_url/$classes_url/$class_name
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | exceptionText_index |
      | 0               | 0                   |

  @internal_error
  Scenario Outline: Deletion of a class when the DB is down_TDAFBA-531
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And the DB has stopped working
    When I delete $base_api_url/$classes_url/$class_name
    Then I get an error response of type 500 with error code SVR1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText            |
      | Generic Server Error(.*) |

    Examples: 
      | old_class_index | exceptionText_index |
      | 0               | 0                   |
