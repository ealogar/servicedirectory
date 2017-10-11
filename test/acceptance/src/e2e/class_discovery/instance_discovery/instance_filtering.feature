# -*- coding: utf-8 -*-
Feature: Instances Filtering
  
  As a class consumer
  I would like the Service Directory to give me the most suitable instance for me, routing the request based on the attributes defining the instance.
  So that I can consume the class
      
  Scenario Outline: Filter instances when the DB is down
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    And the DB has stopped working
    When I request the resource $base_api_url/$classes_url/No_existing_Class/$instances_url with parameters <params_index>:
      | attributes.key1 |
      | trigger_value   |
    Then I get an error response of type 500 with error code SVR1000
    And the exceptionText contains <exceptionText_index>
      | exceptionText            |
      | Generic Server Error(.*) |

    Examples: 
      | old_class_index | old_instance_index | exceptionText_index | params_index |
      | 0               | 0                  | 0                   | 0            |

  @missing_resource
  Scenario Outline: Filter instances over non existing class
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    When I request the resource $base_api_url/$classes_url/No_existing_Class/$instances_url with parameters <params_index>:
      | attributes.key1 |
      | trigger_value   |
    Then I get an error response of type 404 with error code SVC1006
      | exceptionText                |
      | Resource (.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | params_index | exceptionText_index |
      | 0               | 0                  | 0            | 0                   |

  @request
  Scenario Outline: Instances filtering:  No attributes and no instances
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url
    Then I get a success response of type 200 with a result set of size 0

    Examples: 
      | old_class_index |
      | 0               |

  @request
  Scenario Outline: Instances filtering:  No attributes and some instances
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | integration |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                        | environment |
      | v1.0    | http://old.instance.tid.es | integration |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                          | environment |
      | v1.0    | http://newer.instance.tid.es | integration |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v1.0.25 | http://instance.tid.es | integration |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                           | environment |
      | v1.1    | http://backup.instance.tid.es | production  |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                           | environment |
      | v0.9    | http://backup.instance.tid.es | production  |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v4      | http://instance.tid.es | integration |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                           | environment |
      | v1.0    | http://newest.instance.tid.es | integration |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url
    Then I get a success response of type 200 with a result set of size 8
    And the result set contains the instance <instance_index> in position 0:
      | class_name | version | uri                    | environment |
      | Class      | v4      | http://instance.tid.es | integration |
    And the result set contains the instance <instance_index> in position 1:
      | class_name | version | uri                    | environment |
      | Class      | v2.0    | http://instance.tid.es | integration |
    And the result set contains the instance <instance_index> in position 2:
      | class_name | version | uri                           | environment |
      | Class      | v1.1    | http://backup.instance.tid.es | production  |
    And the result set contains the instance <instance_index> in position 3:
      | class_name | version | uri                    | environment |
      | Class      | v1.0.25 | http://instance.tid.es | integration |
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                           | environment |
      | Class      | v1.0    | http://newest.instance.tid.es | integration |
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                          | environment |
      | Class      | v1.0    | http://newer.instance.tid.es | integration |
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                        | environment |
      | Class      | v1.0    | http://old.instance.tid.es | integration |
    And the result set contains the instance <instance_index> in position 7:
      | class_name | version | uri                           | environment |
      | Class      | v0.9    | http://backup.instance.tid.es | production  |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index |
      | 0               | 0                  | 0            | 0              |

  @attibutes_format
  Scenario Outline: Instances filtering:  No existing but valid attributes key
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.1    | http://instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.2    | http://instance.tid.es | production  | key2            | no_trigger_value  |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v3.0    | http://instance.tid.es | production  | key3            | trigger_value     |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | attributes.key1 | attributes.nokey |
      | trigger_value   | trigger_value    |
    Then I get a success response of type 200 with a result set of size 0

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index |
      | 0               | 0                  | 0            | 0              |

  @attibutes_format
  Scenario Outline: Instances filtering:  No existing and non valid attributes key (valid and invalid key)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | attributes.key1 | nokey         |
      | trigger_value   | trigger_value |
    Then I get an error response of type 400 with error code SVC1001
    And the exceptionText contains <exceptionText_index>
      | exceptionText          |
      | Invalid parameter:(.*) |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0                   |

  @attibutes_format
  Scenario Outline: Instances filtering:  No existing and non valid attributes key (single key without .)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | nokey         |
      | trigger_value |
    Then I get an error response of type 400 with error code SVC1001
    And the exceptionText contains <exceptionText_index>
      | exceptionText          |
      | Invalid parameter:(.*) |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0                   |

  @attibutes_format
  Scenario Outline: Instances filtering:  No existing and non valid attributes key (single with .)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | a.nokey       |
      | trigger_value |
    Then I get an error response of type 400 with error code SVC1001
    And the exceptionText contains <exceptionText_index>
      | exceptionText          |
      | Invalid parameter:(.*) |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0                   |

  @attibutes_format
  Scenario Outline: Instances filtering:  No existing and non valid attributes key (empty key)
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | a.nokey       |
      | trigger_value |
    Then I get an error response of type 400 with error code SVC1001
    And the exceptionText contains <exceptionText_index>
      | exceptionText          |
      | Invalid parameter:(.*) |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0                   |

  @attributes_format
  Scenario Outline: Instances filtering:  Repeated keys
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url?attributes.key1=trigger_value&attributes.key1=trigger_value2
    Then I get an error response of type 400 with error code SVC1024
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                |
      | Repeated query parameter: attributes.key1 |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0                   |
      
 @attibutes_format
  Scenario Outline: Instances filtering:  Attributes keys in upper case converted to lower case
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values           |
      | v2.0    | http://instance.tid.es | production  | key1,key2       | trigger_value,trigger_value |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | attributes.key1 | attributes.KEY2 |
      | trigger_value   | trigger_value   |
    Then I get a success response of type 200 with a result set of size 1
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                    | environment | attributes_keys | attributes_values           |
      | Class        | v2.0    | http://instance.tid.es | production  | key1,key2       | trigger_value,trigger_value |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0                   |

  @attibutes_values
  Scenario Outline: Instances filtering:  Empty param
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | attributes.key1 |
      |                 |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Invalid parameter value:(.*) |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0                   |

  @attributes_values
  Scenario Outline: Instances filtering:  Case sensitive and special characters in attributes
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class1     | New Class   | v1.0            |
      | Class2     | New Class   | v1.0            |
      | Class3     | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version                | uri                    | environment            | attributes_keys | attributes_values      |
      | trigger_value !@ñüé./" | http://instance_old.tid.es | trigger_value !@ñüé./" | key1            | trigger_value !@ñüé./" |
    And an instance has already been published with data <old_instance_index>:
      | version                | uri                        | environment            | attributes_keys | attributes_values      |
      | trigger_value !@ñüé./" | http://instance_new.tid.es | trigger_value !@ñüé./" | key1            | trigger_value !@ñüé./" |
    And an instance has already been published with data <old_instance_index>:
      | version                | uri                          | environment            | attributes_keys | attributes_values      |
      | Trigger_value !@ñüé./" | http://old.instance.tid.es | Trigger_value !@ñüé./" | key1            | Trigger_value !@ñüé./" |
    And an instance has already been published with data <old_instance_index>:
      | version                | uri                    | environment            | attributes_keys | attributes_values      |
      | Trigger_value !@ñüé./" | http://new.instance.tid.es | Trigger_value !@ñüé./" | key1            | Trigger_value !@ñüé./" |
    And an instance has already been published with data <old_instance_index>:
      | version                | uri                           | environment            | attributes_keys | attributes_values      |
      | TRIGGER_VALUE !@ñüé./" | http://backupold.instance.tid.es | TRIGGER_VALUE !@ñüé./" | key1            | TRIGGER_VALUE !@ñüé./" |
    And an instance has already been published with data <old_instance_index>:
      | version                | uri                           | environment            | attributes_keys | attributes_values      |
      | TRIGGER_VALUE !@ñüé./" | http://backupnew.instance.tid.es | TRIGGER_VALUE !@ñüé./" | key1            | TRIGGER_VALUE !@ñüé./" |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | attributes.key1        | version                | environment            |
      | trigger_value !@ñüé./" | trigger_value !@ñüé./" | trigger_value !@ñüé./" |
      | Trigger_value !@ñüé./" | Trigger_value !@ñüé./" | Trigger_value !@ñüé./" |
      | TRIGGER_VALUE !@ñüé./" | TRIGGER_VALUE !@ñüé./" | TRIGGER_VALUE !@ñüé./" |
    Then I get a success response of type 200 with a result set of size 2
    And the result set contains the instance <instance_index> in position 0:
      | class_name | version | uri                           | environment | attributes_keys | attributes_values      |
      | Class1     | trigger_value !@ñüé./" | http://instance_old.tid.es | trigger_value !@ñüé./" | key1            | trigger_value !@ñüé./" |
      | Class2     | Trigger_value !@ñüé./" | http://old.instance.tid.es | Trigger_value !@ñüé./" | key1            | Trigger_value !@ñüé./" |
      | Class3     | TRIGGER_VALUE !@ñüé./" | http://backupold.instance.tid.es | TRIGGER_VALUE !@ñüé./" | key1            | TRIGGER_VALUE !@ñüé./" |
    And the result set contains the instance <instance_index> in position 1:
      | class_name | version | uri                           | environment | attributes_keys | attributes_values      |
      | Class1     | trigger_value !@ñüé./" | http://instance_new.tid.es | trigger_value !@ñüé./" | key1            | trigger_value !@ñüé./" |
      | Class2     | Trigger_value !@ñüé./" | http://new.instance.tid.es | Trigger_value !@ñüé./" | key1            | Trigger_value !@ñüé./" |
      | Class3     | TRIGGER_VALUE !@ñüé./" | http://backupnew.instance.tid.es | TRIGGER_VALUE !@ñüé./" | key1            | TRIGGER_VALUE !@ñüé./" |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index |
      | 0               | 0                  | 0            | 0              |
      | 1               | 0                  | 1            | 1              |
      | 2               | 0                  | 2            | 2              |

  @instances_evaluation
  Scenario Outline: Instances filtering: Classes without instances
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | attributes.key1 |
      | trigger_value   |
    Then I get a success response of type 200 with a result set of size 0

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index |
      | 0               | 0                  | 0            | 0              |

  @request
  Scenario Outline: Instances filtering:  Filtered by attributes and some instances ordered
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | integration | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                        | environment | attributes_keys | attributes_values |
      | v1.0    | http://old.instance.tid.es | integration | key2            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                          | environment | attributes_keys | attributes_values |
      | v1.0    | http://newer.instance.tid.es | integration | key2            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v1.0.25 | http://instance.tid.es | integration | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                           | environment | attributes_keys | attributes_values |
      | v1.1    | http://backup.instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                           | environment | attributes_keys | attributes_values |
      | v0.9    | http://backup.instance.tid.es | production  | key2            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v4      | http://instance.tid.es | integration | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                           | environment | attributes_keys | attributes_values |
      | v1.0    | http://newest.instance.tid.es | integration | key2            | trigger_value     |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | attributes.key1 |
      | trigger_value   |
    Then I get a success response of type 200 with a result set of size 4
    And the result set contains the instance <instance_index> in position 0:
      | class_name | version | uri                    | environment | attributes_keys | attributes_values |
      | Class      | v4      | http://instance.tid.es | integration | key1            | trigger_value     |
    And the result set contains the instance <instance_index> in position 1:
      | class_name | version | uri                    | environment | attributes_keys | attributes_values |
      | Class      | v2.0    | http://instance.tid.es | integration | key1            | trigger_value     |
    And the result set contains the instance <instance_index> in position 2:
      | class_name | version | uri                           | environment | attributes_keys | attributes_values |
      | Class      | v1.1    | http://backup.instance.tid.es | production  | key1            | trigger_value     |
    And the result set contains the instance <instance_index> in position 3:
      | class_name | version | uri                    | environment | attributes_keys | attributes_values |
      | Class      | v1.0.25 | http://instance.tid.es | integration | key1            | trigger_value     |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index |
      | 0               | 0                  | 0            | 0              |

  @environment
  Scenario Outline: Instances filtering: Filtering with environment
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class1     | New Class   | v1.0            |
      | Class2     | New Class   | v1.0            |
      | Class3     | New Class   | v1.0            |
      | Class4     | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.1    | http://instance.tid.es | integration | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | attributes_keys | attributes_values |
      | v2.2    | http://instance.tid.es | [STRING_WITH_LENGTH_511] | key1            | no_trigger_value  |
    And an instance has already been published with data <old_instance_index>::
      | version | uri                    | environment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | attributes_keys | attributes_values |
      | v3.0    | http://instance.tid.es | [STRING_WITH_LENGTH_512] | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v4.0    | http://instance.tid.es | p           | key1            | no_trigger_value  |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | environment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
      | production                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
      | [STRING_WITH_LENGTH_511] |
      | [STRING_WITH_LENGTH_512]  |
      | p                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
    Then I get a success response of type 200 with a result set of size 1
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                    | environment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | attributes_keys | attributes_values |
      | Class1     | v2.0    | http://instance.tid.es | production                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | key1            | trigger_value     |
      | Class2     | v2.2    | http://instance.tid.es | [STRING_WITH_LENGTH_511] | key1            | no_trigger_value  |
      | Class3     | v3.0    | http://instance.tid.es | [STRING_WITH_LENGTH_512]  | key1            | trigger_value     |
      | Class4     | v4.0    | http://instance.tid.es | p                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | key1            | no_trigger_value  |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index |
      | 0               | 0                  | 0            | 0              |
      | 1               | 0                  | 1            | 1              |
      | 2               | 0                  | 2            | 2              |
      | 3               | 0                  | 3            | 3              |

  @environment
  @bug(APIDIRSVR-460)
  Scenario Outline: Instances filtering: Environment filtering limitations
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.1    | http://instance.tid.es | integration | key1            | trigger_value     |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | environment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
      | [STRING_WITH_LENGTH_512] |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Invalid parameter value:(.*) |

    Examples: 
      | old_class_index | old_instance_index | params_index | exceptionText_index |
      | 0               | 0                  | 0            | 0                   |

  @version
  Scenario Outline: Instances filtering: Filtering with version
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class1     | New Class   | v1.0            |
      | Class2     | New Class   | v1.0            |
      | Class3     | New Class   | v1.0            |
      | Class4     | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.1    | http://instance.tid.es | integration | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version                                                                                                                                                                                                                                                         | uri                       | environment | attributes_keys | attributes_values |
      | [STRING_WITH_LENGTH_255] | http://instancenew.tid.es | production  | key1            | no_trigger_value  |
    And an instance has already been published with data <old_instance_index>::
      | version                                                                                                                                                                                                                                                          | uri                    | environment | attributes_keys | attributes_values |
      | [STRING_WITH_LENGTH_256] | http://instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v       | http://instance.tid.es | production  | key1            | no_trigger_value  |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | version                                                                                                                                                                                                                                                          |
      | v2.0                                                                                                                                                                                                                                                             |
      | [STRING_WITH_LENGTH_255]  |
      | [STRING_WITH_LENGTH_256] |
      | v                                                                                                                                                                                                                                                                |
    Then I get a success response of type 200 with a result set of size 1
    And the result set contains the instance <instance_index>:
      | class_name | version                                                                                                                                                                                                                                                          | uri                       | environment | attributes_keys | attributes_values |
      | Class1     | v2.0                                                                                                                                                                                                                                                             | http://instance.tid.es    | production  | key1            | trigger_value     |
      | Class2     | [STRING_WITH_LENGTH_255]  | http://instancenew.tid.es | production  | key1            | no_trigger_value  |
      | Class3     | [STRING_WITH_LENGTH_256] | http://instance.tid.es    | production  | key1            | trigger_value     |
      | Class4     | v                                                                                                                                                                                                                                                                | http://instance.tid.es    | production  | key1            | no_trigger_value  |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index |
      | 0               | 0                  | 0            | 0              |
      | 1               | 0                  | 1            | 1              |
      | 2               | 0                  | 2            | 2              |
      | 3               | 0                  | 3            | 3              |

  @version
  @bug(APIDIRSVR-461)
  Scenario Outline: Instances filtering: Version filtering limitations
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.1    | http://instance.tid.es | integration | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                       | environment | attributes_keys | attributes_values |
      | v2.0    | http://instancenew.tid.es | production  | key1            | no_trigger_value  |
    And an instance has already been published with data <old_instance_index>::
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v3.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v4.0    | http://instance.tid.es | production  | key1            | no_trigger_value  |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | version                                                                                                                                                                                                                                                           |
      | [STRING_WITH_LENGTH_255] |
      |                                                                                                                                                                                                                                                                   |
    Then I get an error response of type 400 with error code SVC0002
    And the exceptionText contains <exceptionText_index>
      | exceptionText                |
      | Invalid parameter value:(.*) |

    Examples: 
      | old_class_index | old_instance_index | params_index | exceptionText_index |
      | 0               | 0                  | 0            | 0                   |
      | 0               | 0                  | 1            | 0                   |

  @single_attributes
  Scenario Outline: Instances filtering: single valid attributes not all results filtered
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.1    | http://instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.2    | http://instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v3.0    | http://instance.tid.es | production  | key2            | no_trigger_value  |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v4.0    | http://instance.tid.es | production  | key2            | no_trigger_value  |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | attributes.key1  |
      | no_trigger_value |
    Then I get a success response of type 200 with a result set of size 0

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index |
      | 0               | 0                  | 0            | 0              |

  @multi_attributes
  Scenario Outline: Instances filtering: multiple valid attributes in all instances that generates 0 results
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    Given a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values                            |
      | v2.0    | http://instance.tid.es | production  | key1,key2,key3  | trigger_value,trigger_value,no_trigger_value |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values                             |
      | v2.1    | http://instance.tid.es | production  | key1,key2,key3  | trigger_value, no_trigger_value,trigger_value |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values                                  |
      | v2.2    | http://instance.tid.es | production  | key1,key2,key3  | no_trigger_value,no_trigger_value,no_trigger_value |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | attributes.key1 | attributes.key2 | attributes.key3 |
      | trigger_value   | trigger_value   | trigger_value   |
    Then I get a success response of type 200 with a result set of size 0

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index |
      | 0               | 0                  | 0            | 0              |

  @multi_attributes
  Scenario Outline: Instances filtering: multiple valid attributes not in all instances that generates 0 results
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.0    | http://instance.tid.es | production  | key1            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.1    | http://instance.tid.es | production  | key2            | trigger_value     |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values |
      | v2.2    | http://instance.tid.es | production  | key3            | trigger_value     |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | attributes.key1 | attributes.key2 | attributes.key3 |
      | trigger_value   | trigger_value   | trigger_value   |
    Then I get a success response of type 200 with a result set of size 0

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index |
      | 0               | 0                  | 0            | 0              |

  @multi_attributes
  Scenario Outline: Instances filtering: multiple valid attributes not in all instances that generates some results
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values                         |
      | v2.0    | http://instance.tid.es | production  | key1,key2,key3  | trigger_value,trigger_value,trigger_value |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values                             |
      | v2.1    | http://instance.tid.es | production  | key1,key2,key3  | trigger_value, trigger_value,no_trigger_value |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values                                  |
      | v2.2    | http://instance.tid.es | production  | key1,key2,key3  | no_trigger_value,no_trigger_value,no_trigger_value |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | attributes.key1 | attributes.key2 | attributes.key3 |
      | trigger_value   | trigger_value   | trigger_value   |
    Then I get a success response of type 200 with a result set of size 1
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                    | environment | attributes_keys | attributes_values                         |
      | Class      | v2.0    | http://instance.tid.es | production  | key1,key2,key3  | trigger_value,trigger_value,trigger_value |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index |
      | 0               | 0                  | 0            | 0              |

  @happy_path
  Scenario Outline: Instances filtering: attributes, version and environment query and some results filtered
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0            |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                     | environment | attributes_keys | attributes_values           |
      | v2.0    | http://instanceA.tid.es | production  | key1,key2       | trigger_value,trigger_value |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                     | environment | attributes_keys | attributes_values           |
      | v2.0    | http://instanceB.tid.es | production  | key1,key2       | trigger_value,trigger_value |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                      | environment | attributes_keys | attributes_values               |
      | v2.0    | http://instanceAB.tid.es | production  | key1,key2       | trigger_value,non_trigger_value |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                     | environment | attributes_keys | attributes_values           |
      | v2.0    | http://instanceBC.tid.es | test        | key1,key2       | trigger_value,trigger_value |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values           |
      | v2.2    | http://instance.tid.es | production  | key1,key2       | trigger_value,trigger_value |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values           |
      | v3.0    | http://instance.tid.es | production  | key1,key2       | trigger_value,trigger_value |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment | attributes_keys | attributes_values           |
      | v4.0    | http://instance.tid.es | production  | key1,key2       | trigger_value,trigger_value |
    When I request the resource $base_api_url/$classes_url/$class_name/$instances_url with parameters <params_index>:
      | attributes.key1 | attributes.key2 | environment | version |
      | trigger_value   | trigger_value   | production  | v2.0    |
    Then I get a success response of type 200 with a result set of size 2
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                     | environment | attributes_keys | attributes_values           |
      | Class      | v2.0    | http://instanceA.tid.es | production  | key1,key2       | trigger_value,trigger_value |
      | Class      | v2.0    | http://instanceB.tid.es | production  | key1,key2       | trigger_value,trigger_value |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index |
      | 0               | 0                  | 0            | 0              |
