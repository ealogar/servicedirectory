# -*- coding: utf-8 -*-
Feature: Instance Discovering
  
  As a class consumer
  I would like the Service Directory to give me the most suitable instance for me, routing the request based on the attributes defining the instance.
  So that I can consume the class

  @eq_rules
  Scenario Outline: Discovery instance with eq rules and trigerring values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value       |
      | eq        | test_param          | 1           |
      | eq        | test_param          | hello       |
      | eq        | test_param          | " "         |
      | eq        | test_param          | España cañí |
      | eq        | test_param          | 10.5        |
      | eq        | test_param          | true        |
      | eq        | test_param          | [TRUE] |
    And the previous bindings are published for the context <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
      | Origin4 | Class      |
      | Origin5 | Class      |
      | Origin6 | Class      |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin  | test_param  | class_name |
      | Origin0 | 1           | Class      |
      | Origin1 | hello       | Class      |
      | Origin2 | " "         | Class      |
      | Origin3 | España cañí | Class      |
      | Origin4 | 10.5        | Class      |
      | Origin5 | true        | Class      |
      | Origin6 | true        | Class      |
    Then I get a success response of type 200
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                    | environment |
      | Class      | v2.0    | http://instance.tid.es | production  |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | binding_index | rule_index |
      | 0               | 0                  | 0            | 0              | 0             | 0          |
      | 0               | 0                  | 1            | 0              | 1             | 1          |
      | 0               | 0                  | 2            | 0              | 2             | 2          |
      | 0               | 0                  | 3            | 0              | 3             | 3          |
      | 0               | 0                  | 4            | 0              | 4             | 4          |
      | 0               | 0                  | 5            | 0              | 5             | 5          |
      | 0               | 0                  | 6            | 0              | 6             | 6          |

  @eq_rules
  Scenario Outline: Discovery instance with eq rules and non trigerring values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value       |
      | eq        | test_param          | 1           |
      | eq        | test_param          | hello       |
      | eq        | test_param          | "  "        |
      | eq        | test_param          | España cañí |
      | eq        | test_param          | 10.5        |
    And the previous bindings are published for the context <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
      | Origin4 | Class      |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin  | test_param | class_name |
      | Origin0 | 2          | Class      |
      | Origin0 | -1         | Class      |
      | Origin0 | v1.0        | Class      |
      | Origin0 | "1"        | Class      |
      | Origin1 | Hello      | Class      |
      | Origin1 | hellow     | Class      |
      | Origin1 | he llo     | Class      |
      | Origin2 | " "        | Class      |
      | Origin3 | España     | Class      |
      | Origin4 | 10,5       | Class      |
      | Origin4 | 10         | Class      |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                    |
      | Resource binding-Class-Origin(.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | binding_index | rule_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0             | 0          | 0                   |
      | 0               | 0                  | 1            | 0              | 0             | 0          | 0                   |
      | 0               | 0                  | 2            | 0              | 0             | 0          | 0                   |
      | 0               | 0                  | 3            | 0              | 0             | 0          | 0                   |
      | 0               | 0                  | 4            | 0              | 1             | 1          | 0                   |
      | 0               | 0                  | 5            | 0              | 1             | 1          | 0                   |
      | 0               | 0                  | 6            | 0              | 1             | 1          | 0                   |
      | 0               | 0                  | 7            | 0              | 2             | 2          | 0                   |
      | 0               | 0                  | 8            | 0              | 3             | 3          | 0                   |
      | 0               | 0                  | 9            | 0              | 4             | 4          | 0                   |
      | 0               | 0                  | 10           | 0              | 4             | 4          | 0                   |

  @range_rules
  Scenario Outline: Discovery instance with range rules and trigerring values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value     |
      | range     | test_param          | 10,20     |
      | range     | test_param          | 1.0,3.0   |
      | range     | test_param          | -1,1      |
      | range     | test_param          | -1.5,1.6  |
      | range     | test_param          | -200,-100 |
      | range     | test_param          | a,c       |
      | range     | test_param          | A,c       |
    And the previous bindings are published for the context <binding_index>:
      | origin   | class_name |
      | Origin0  | Class      |
      | Origin1  | Class      |
      | Origin2  | Class      |
      | Origin3  | Class      |
      | Origin4  | Class      |
      | Origin5  | Class      |
      | Origin6  | Class      |
      | Origin7  | Class      |
      | Origin8  | Class      |
      | Origin9  | Class      |
      | Origin10 | Class      |
      | Origin11 | Class      |
      | Origin12 | Class      |
      | Origin13 | Class      |
      | Origin14 | Class      |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin   | test_param | class_name |
      | Origin0  | 15         | Class      |
      | Origin1  | 10         | Class      |
      | Origin2  | 20         | Class      |
      | Origin3  | 2.0        | Class      |
      | Origin4  | 1.0        | Class      |
      | Origin5  | 0          | Class      |
      | Origin6  | -1         | Class      |
      | Origin7  | -1.5       | Class      |
      | Origin8  | 0.0        | Class      |
      | Origin9  | 1.45       | Class      |
      | Origin10 | -150       | Class      |
      | Origin11 | b          | Class      |
      | Origin12 | abc        | Class      |
      | Origin13 | a          | Class      |
      | Origin14 | a          | Class      |
    Then I get a success response of type 200
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                    | environment |
      | Class      | v2.0    | http://instance.tid.es | production  |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | binding_index | rule_index |
      | 0               | 0                  | 0            | 0              | 0             | 0          |
      | 0               | 0                  | 1            | 0              | 1             | 0          |
      | 0               | 0                  | 2            | 0              | 2             | 0          |
      | 0               | 0                  | 3            | 0              | 3             | 1          |
      | 0               | 0                  | 4            | 0              | 4             | 1          |
      | 0               | 0                  | 5            | 0              | 5             | 2          |
      | 0               | 0                  | 6            | 0              | 6             | 2          |
      | 0               | 0                  | 7            | 0              | 7             | 3          |
      | 0               | 0                  | 8            | 0              | 8             | 3          |
      | 0               | 0                  | 9            | 0              | 9             | 3          |
      | 0               | 0                  | 10           | 0              | 10            | 4          |
      | 0               | 0                  | 11           | 0              | 11            | 5          |
      | 0               | 0                  | 12           | 0              | 12            | 5          |
      | 0               | 0                  | 13           | 0              | 13            | 5          |
      | 0               | 0                  | 14           | 0              | 14            | 6          |

  @range_rules
  Scenario Outline: Discovery instance with range rules and no trigerring values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value       |
      | range     | test_param          | 10.0,20.0   |
      | range     | test_param          | 10,20       |
      | range     | test_param          | -1,1        |
      | range     | test_param          | 1.5,1.6     |
      | range     | test_param          | a,c         |
      | range     | test_param          | 1,214748364 |
    And the previous bindings are published for the context <binding_index>:
      | origin   | class_name |
      | Origin0  | Class      |
      | Origin1  | Class      |
      | Origin2  | Class      |
      | Origin3  | Class      |
      | Origin4  | Class      |
      | Origin5  | Class      |
      | Origin6  | Class      |
      | Origin7  | Class      |
      | Origin8  | Class      |
      | Origin9  | Class      |
      | Origin10 | Class      |
      | Origin11 | Class      |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin   | test_param   | class_name |
      | Origin0  | 9.9999999999 | Class      |
      | Origin1  | 20.09        | Class      |
      | Origin2  | 21           | Class      |
      | Origin3  | 9            | Class      |
      | Origin4  | 2            | Class      |
      | Origin5  | -2           | Class      |
      | Origin6  | 1.49999999   | Class      |
      | Origin7  | z            | Class      |
      | Origin8  | d            | Class      |
      | Origin9  | ca           | Class      |
      | Origin10 | -2147483648  | Class      |
      | Origin11 | 2147483648   | Class      |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                    |
      | Resource binding-Class-Origin(.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | binding_index | rule_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0             | 0          | 0                   |
      | 0               | 0                  | 1            | 0              | 1             | 0          | 0                   |
      | 0               | 0                  | 2            | 0              | 2             | 1          | 0                   |
      | 0               | 0                  | 3            | 0              | 3             | 1          | 0                   |
      | 0               | 0                  | 4            | 0              | 4             | 2          | 0                   |
      | 0               | 0                  | 5            | 0              | 5             | 2          | 0                   |
      | 0               | 0                  | 6            | 0              | 6             | 3          | 0                   |
      | 0               | 0                  | 7            | 0              | 7             | 4          | 0                   |
      | 0               | 0                  | 8            | 0              | 8             | 4          | 0                   |
      | 0               | 0                  | 9            | 0              | 9             | 4          | 0                   |
      | 0               | 0                  | 10           | 0              | 10            | 5          | 0                   |
      | 0               | 0                  | 11           | 0              | 11            | 5          | 0                   |

  @range_rules
  Scenario Outline: Discovery instance with range rules and non valid values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value   |
      | range     | test_param          | 10,20   |
      | range     | test_param          | 1.0,3.0 |
    And the previous bindings are published for the context <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin  | test_param | class_name |
      | Origin0 | 5.0        | Class      |
      | Origin1 | 2          | Class      |
      | Origin2 | a          | Class      |
      | Origin3 | true       | Class      |
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                             |
      | Invalid parameter value: (.*). Supported values are: (.*) |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | binding_index | rule_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0             | 0          | 0                   |
      | 0               | 0                  | 1            | 0              | 1             | 1          | 0                   |
      | 0               | 0                  | 2            | 0              | 2             | 1          | 0                   |
      | 0               | 0                  | 3            | 0              | 3             | 1          | 0                   |

  #TODO: Search a way to pass from parameter a boolean type {"test_param" : True} and keep it json format using lowercase {u'test_param' : true}
  @in_rules
  Scenario Outline: Discovery instance with in rules and trigerring values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value                             |
      | in        | test_param          | 10,20                             |
      | in        | test_param          | 0.0,-1.0                          |
      | in        | test_param          | es*,España                        |
      | in        | test_param          | Alone                             |
      | in        | test_param          | a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q |
      | in        | test_param          | 1.5,1.6,2.0                       |
      | in        | test_param          | true,false                        |
      | in        | test_param          | True,False                        |
    And the previous bindings are published for the context <binding_index>:
      | origin   | class_name |
      | Origin0  | Class      |
      | Origin1  | Class      |
      | Origin2  | Class      |
      | Origin3  | Class      |
      | Origin4  | Class      |
      | Origin5  | Class      |
      | Origin6  | Class      |
      | Origin7  | Class      |
      | Origin8  | Class      |
      | Origin9  | Class      |
      | Origin10 | Class      |
      | Origin11 | Class      |
      | Origin12 | Class      |
      | Origin13 | Class      |
      | Origin14 | Class      |
      | Origin15 | Class      |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin   | test_param | class_name |
      | Origin0  | 10         | Class      |
      | Origin1  | 20         | Class      |
      | Origin2  | 0.0        | Class      |
      | Origin3  | -1.0       | Class      |
      | Origin4  | es*        | Class      |
      | Origin5  | España     | Class      |
      | Origin6  | Alone      | Class      |
      | Origin7  | a          | Class      |
      | Origin8  | h          | Class      |
      | Origin9  | q          | Class      |
      | Origin10 | 1.5        | Class      |
      | Origin11 | 2.0        | Class      |
      | Origin12 | true       | Class      |
      | Origin13 | false      | Class      |
      | Origin14 | True       | Class      |
      | Origin15 | False      | Class      |
    Then I get a success response of type 200
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                    | environment |
      | Class      | v2.0    | http://instance.tid.es | production  |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | binding_index | rule_index |
      | 0               | 0                  | 0            | 0              | 0             | 0          |
      | 0               | 0                  | 1            | 0              | 1             | 0          |
      | 0               | 0                  | 2            | 0              | 2             | 1          |
      | 0               | 0                  | 3            | 0              | 3             | 1          |
      | 0               | 0                  | 4            | 0              | 4             | 2          |
      | 0               | 0                  | 5            | 0              | 5             | 2          |
      | 0               | 0                  | 6            | 0              | 6             | 3          |
      | 0               | 0                  | 7            | 0              | 7             | 4          |
      | 0               | 0                  | 8            | 0              | 8             | 4          |
      | 0               | 0                  | 9            | 0              | 9             | 4          |
      | 0               | 0                  | 10           | 0              | 10            | 5          |
      | 0               | 0                  | 11           | 0              | 11            | 5          |
      | 0               | 0                  | 12           | 0              | 12            | 6          |
      | 0               | 0                  | 13           | 0              | 13            | 6          |
      | 0               | 0                  | 14           | 0              | 14            | 7          |
      | 0               | 0                  | 15           | 0              | 15            | 7          |

  @in_rules
  Scenario Outline: Discovery instance with in rules and no trigerring values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0     | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value       |
      | in        | test_param          | 10,20       |
      | in        | test_param          | a,b         |
      | in        | test_param          | es*,España  |
      | in        | test_param          | Alone       |
      | in        | test_param          | v1.5,v1.6,v2.0 |
      | in        | test_param          | [TRUE] |
    And the previous bindings are published for the context <binding_index>:
      | origin   | class_name |
      | Origin0  | Class      |
      | Origin1  | Class      |
      | Origin2  | Class      |
      | Origin3  | Class      |
      | Origin4  | Class      |
      | Origin5  | Class      |
      | Origin6  | Class      |
      | Origin7  | Class      |
      | Origin8  | Class      |
      | Origin9  | Class      |
      | Origin10 | Class      |
      | Origin11 | Class      |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin   | test_param | class_name |
      | Origin0  | 5          | Class      |
      | Origin1  | 0          | Class      |
      | Origin2  | -10        | Class      |
      | Origin3  | c          | Class      |
      | Origin4  | A          | Class      |
      | Origin5  | ä          | Class      |
      | Origin6  | est        | Class      |
      | Origin7  | Not_Alone  | Class      |
      | Origin8  | 1.55       | Class      |
      | Origin9  | 2.00000005 | Class      |
      | Origin10 | -1.55      | Class      |
      | Origin11 | false      | Class      |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                    |
      | Resource binding-Class-Origin(.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | binding_index | rule_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0             | 0          | 0                   |
      | 0               | 0                  | 1            | 0              | 1             | 0          | 0                   |
      | 0               | 0                  | 2            | 0              | 2             | 0          | 0                   |
      | 0               | 0                  | 3            | 0              | 3             | 1          | 0                   |
      | 0               | 0                  | 4            | 0              | 4             | 1          | 0                   |
      | 0               | 0                  | 5            | 0              | 5             | 1          | 0                   |
      | 0               | 0                  | 6            | 0              | 6             | 2          | 0                   |
      | 0               | 0                  | 7            | 0              | 7             | 3          | 0                   |
      | 0               | 0                  | 8            | 0              | 8             | 4          | 0                   |
      | 0               | 0                  | 9            | 0              | 9             | 4          | 0                   |
      | 0               | 0                  | 10           | 0              | 10            | 4          | 0                   |
      | 0               | 0                  | 11           | 0              | 11            | 5          | 0                   |

  @in_rules
  Scenario Outline: Discovery instance with in rules and non valid values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value       |
      | in        | test_param          | 10,20       |
      | in        | test_param          | 1.5,1.6,2.0 |
      | in        | test_param          | [TRUE] |
    And the previous bindings are published for the context <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin  | test_param | class_name |
      | Origin0 | 10.0       | Class      |
      | Origin1 | 2          | Class      |
      | Origin2 | 1          | Class      |
      | Origin3 | 2          | Class      |
    Then I get an error response of type 400 with error code SVC1021
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                             |
      | Invalid parameter value: (.*). Supported values are: (.*) |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | binding_index | rule_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0             | 0          | 0                   |
      | 0               | 0                  | 1            | 0              | 1             | 1          | 0                   |
      | 0               | 0                  | 2            | 0              | 2             | 2          | 0                   |
      | 0               | 0                  | 3            | 0              | 3             | 2          | 0                   |

  @regex_rules
  Scenario Outline: Discovery instance with regex rules and trigerring values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value      |
      | regex     | test_param          | (.*)       |
      | regex     | test_param          | (\d+)     |
      | regex     | test_param          | [A-Za-z]*$ |
    And the previous bindings are published for the context <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
      | Origin4 | Class      |
      | Origin5 | Class      |
      | Origin6 | Class      |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin  | test_param | class_name |
      | Origin0 | 20         | Class      |
      | Origin1 | " "        | Class      |
      | Origin2 | free text  | Class      |
      | Origin3 | 10         | Class      |
      | Origin4 | LeTteRs    | Class      |
    Then I get a success response of type 200
    And the result set contains the instance <instance_index>:
      | class_name | version | uri                    | environment |
      | Class      | v2.0    | http://instance.tid.es | production  |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | binding_index | rule_index |
      | 0               | 0                  | 0            | 0              | 0             | 0          |
      | 0               | 0                  | 1            | 0              | 1             | 0          |
      | 0               | 0                  | 2            | 0              | 2             | 0          |
      | 0               | 0                  | 3            | 0              | 3             | 1          |
      | 0               | 0                  | 4            | 0              | 4             | 2          |

  @regex_rules
  Scenario Outline: Discovery instance with regex rules and no trigerring values
    Given the user performing the operation is:
      | username | password |
      | admin    | admin    |
    And a class has already been published with data <old_class_index>:
      | class_name | description | default_version |
      | Class      | New Class   | v1.0             |
    And an instance has already been published with data <old_instance_index>:
      | version | uri                    | environment |
      | v2.0    | http://instance.tid.es | production  |
    And the following bindings rules are available <rule_index>:
      | operation | input_context_param | value      |
      | regex     | test_param          | (\\d+)     |
      | regex     | test_param          | [A-Za-z]*$ |
    And the previous bindings are published for the context <binding_index>:
      | origin  | class_name |
      | Origin0 | Class      |
      | Origin1 | Class      |
      | Origin2 | Class      |
      | Origin3 | Class      |
      | Origin4 | Class      |
    When I request the resource $base_api_url/$bind_instances_url with parameters <params_index>:
      | origin  | test_param | class_name |
      | Origin0 | test       | Class      |
      | Origin1 | test 1     | Class      |
      | Origin2 | 97         | Class      |
      | Origin3 | Test 1     | Class      |
      | Origin3 | ""         | Class      |
    Then I get an error response of type 404 with error code SVC1006
    And the exceptionText contains <exceptionText_index>
      | exceptionText                                    |
      | Resource binding-Class-Origin(.*) does not exist |

    Examples: 
      | old_class_index | old_instance_index | params_index | instance_index | binding_index | rule_index | exceptionText_index |
      | 0               | 0                  | 0            | 0              | 0             | 0          | 0                   |
      | 0               | 0                  | 1            | 0              | 1             | 0          | 0                   |
      | 0               | 0                  | 2            | 0              | 2             | 1          | 0                   |
      | 0               | 0                  | 3            | 0              | 3             | 1          | 0                   |
      | 0               | 0                  | 4            | 0              | 3             | 1          | 0                   |
