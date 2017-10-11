# -*- coding: utf-8 -*-
Feature: List Service Class Collection
  
  As a class provider
  I would like to be able to list all the classes exposed by the Service Directory


  @happy_path
  Scenario Outline: List the classes exposed by the Service Directory
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | default_version |
      | Class1      | v1.0             |
    And another class has already been published with data <old_class_index>:
      | class_name | default_version |
      | Class2      | v2.0             |
    When I get the service class collection $base_api_url/$classes_url
    Then I get a success response of type 200
    And the collection contains the class Class1
    And the collection contains the class Class2

    Examples: 
      | old_class_index | 
      | 0               | 


  @updated_list
  Scenario Outline: List a class deleted on service collection class published
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | default_version |
      | Class      | v1.0             |
    And I delete $base_api_url/$classes_url/$class_name
    And I get a success response of type 204
    When I get the service class collection $base_api_url/$classes_url
    Then the collection not contains the class $class_name

    Examples: 
      | old_class_index |
      | 0               |

  @internal_error
  Scenario Outline: List the collection of classes when the DB is down
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0             |
    And the DB has stopped working
    When I request the resource $base_api_url/$classes_url
    Then I get an error response of type 500 with error code SVR1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText            |
      | Generic Server Error(.*) |

    Examples: 
      | old_class_index | exceptionText_index |
      | 0               | 0                   |
      
  @wrong_header
  Scenario Outline: Request something using a not valid Accept header
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | class      | class       | v1.0            |
    When I request the resource $base_api_url/$classes_url with headers <headers_index>:
      | Accept     |
      | text/html  |
    Then I get an error response of type 406


    Examples: 
      | old_class_index | exceptionText_index | headers_index |
      | 0               | 0                   | 0             |
