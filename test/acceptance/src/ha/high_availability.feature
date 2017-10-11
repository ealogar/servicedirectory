# -*- coding: utf-8 -*-
Feature: High Availability
  
  As a Service deployed in HA
  I want to use the service transparently to the deployment configuration
  so if a frontend or a backend is stopped for some reason, the service is not affected.

  @happy_path
  Scenario Outline: (1) Once of frontend server fails
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0            |
    When the frontend 0 has stopped working
    And I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
            | v2.0    | http://instance.tid.es |
    Then I get a success response of type 201 with location <location_index>:
      | location                                                     |
      | $base_api_url/$classes_url/$class_name/$instances_url/(\w+) |
    And the response contains the instance data
    And the frontend 0 is working
    And the location returns the instance data
    And the location returns the instance data
    
    Examples: 
      | old_class_index | instance_index | location_index | 
      | 0               | 0              | 0              | 
      | 0               | 1              | 0              |  
           
  @happy_path
  Scenario Outline: (2) The primary MongoDB fails
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0            |
    And wait while the content is replicated
    When the primary MongoDB has stopped working
    And wait while the replicaset know this change
    And I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    Then I get a success response of type 201 with location <location_index>:
      | location                                                     |
      | $base_api_url/$classes_url/$class_name/$instances_url/(\w+) |


    Examples: 
      | old_class_index | instance_index | location_index | 
      | 0               | 0              | 0              | 

  Scenario Outline: (3) The primary MongoDB fails and restart again its service
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0            |
    And wait while the content is replicated
    And the primary MongoDB has stopped working
    And wait while the replicaset know this change
    And I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    And I get a success response of type 201 with location <location_index>:
      | location                                                     |
      | $base_api_url/$classes_url/$class_name/$instances_url/(\w+) |
    When the mongodb tested is restarted
    Then I request the resource $base_api_url/$classes_url/$class_name/$instances_url
    And I get a success response of type 200 with a result set of size 1
    And I request the resource $base_api_url/$classes_url/$class_name/$instances_url
    And I get a success response of type 200 with a result set of size 1
    
    Examples: 
      | old_class_index | instance_index | location_index | 
      | 0               | 0              | 0              | 

  Scenario Outline: (4) Both frontend servers fails
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0            |
    When the frontend 0 has stopped working
    And the frontend 1 has stopped working
    And the frontend 0 is working
    And the frontend 1 is working
    And I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    Then I get a success response of type 201 with location <location_index>:
      | location                                                     |
      | $base_api_url/$classes_url/$class_name/$instances_url/(\w+) |
    And the response contains the instance data
    And the location returns the instance data

    Examples: 
      | old_class_index | instance_index | location_index | 
      | 0               | 0              | 0              | 


  Scenario Outline: (5) All MongoDB servers are restarted and the replicaset is reconfigured correctly
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0            |
    And all MongoDB has stopped working
    When all MongoDB are working
    And wait while the replicaset know this change
    And I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    Then I get a success response of type 201 with location <location_index>:
      | location                                                     |
      | $base_api_url/$classes_url/$class_name/$instances_url/(\w+) |
    And the response contains the instance data
    And the location returns the instance data

    Examples: 
      | old_class_index | instance_index | location_index | 
      | 0               | 0              | 0              | 
  
  Scenario Outline: (6) The primary MongoDB and one of secondary MongoDB server are stopped
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0            |
    And wait while the content is replicated
    When the primary MongoDB has stopped working
    And another MongoDB has stopped working
    And wait while the replicaset know this change
    And I request the resource $base_api_url/$classes_url
    And I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    Then I get an error response of type 500 with error code SVR1000

    Examples: 
      | old_class_index | instance_index | location_index | 
      | 0               | 0              | 0              | 
      
  Scenario Outline: (7) Once of frontend server restarts after a fail during primary MongoDB is down
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | Class       | v1.0            |
    When the frontend 0 has stopped working
    And the frontend 1 has stopped working
    And the primary MongoDB has stopped working
    When the frontend 1 is working
    And wait while the replicaset know this change
    And I request the resource $base_api_url/$classes_url
    And I send to $base_api_url/$classes_url/$class_name/$instances_url the instance data <instance_index>:
      | version | uri                    |
      | v1.0    | http://instance.tid.es |
    Then I get a success response of type 201 with location <location_index>:
      | location                                                     |
      | $base_api_url/$classes_url/$class_name/$instances_url/(\w+) |
    And the response contains the instance data
    And the location returns the instance data


    Examples: 
      | old_class_index | instance_index | location_index |
      | 0               | 0              | 0              |

  @reliability
  Scenario Outline: (8) Once of frontend server fails, check the time to be stabilized 
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And monitoring balancer while request timeout more than 300 milliseconds
    When the frontend 0 has stopped working
    Then wait while monitoring is not stabilized
    And time unstable is less than 10 seconds
    And stop monitoring balancer
    
  @reliability
  Scenario Outline: (9) The primary MongoDB fails, check the time to reconfigure replicaset
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And monitoring balancer while request timeout more than 300 milliseconds
    When the primary MongoDB has stopped working
    Then wait while monitoring is not stabilized
    And time unstable is less than 30 seconds
    And stop monitoring balancer
    
      
 # Scenario Outline: Frontend lose the connectivity with all MongoDBs
 #   Given the frontend 0 is working
 #   When all MongoDB has stopped working
 #   Then the frontend 0 is not a valid IP for balancer

 # Scenario Outline: An instance of MongoDB Server recovers its availability in a short time of period
 #   Given the primary MongoDB has stopped working
 #   When the MongoDB tested is working
 #   Then the time to recover the mongodb is less than 10 seconds

 # Scenario Outline: An instance of Frontend Server recovers its availability in a short time of period
 #   Given the frontend 0 has stopped working
 #   When the frontend 0 is working
 #   Then the time to recover the frontend is less than 10 seconds
