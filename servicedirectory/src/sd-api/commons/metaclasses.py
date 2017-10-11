'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from inspect import isfunction


def decorate(decorated_func_name, decorated_function, decorating_functions):
    for decorate_function in decorating_functions:
        function = decorate_function(decorated_func_name, decorated_function)
    return function


def decorate_methods(*decorating_functions):
    """
    Metaclass to decorate all member functions with a set of decorators.
    The methods will be decorated in the order defined in set.

    You must provide a custom function with two arguments (name and function).
    The function can implement logic inside to apply decorator to function or
    not, and return the result (decorated function or not).
     e.g:
        def apply_or_not(name,function):
            if name == 'my_name':
                 return decorator(function)
            return function

    :param decorating_functions a variable list of decorators_functions to apply or
           functions with name, function as argument to apply decorator or no
           given a custom logic.
    """
    class DecorateMetaClass(type):
        def __new__(meta, classname, supers, classdict):  # @NoSelf
            for attr, attrval in classdict.items():
                if isfunction(attrval):
                    classdict[attr] = decorate(attr, attrval, decorating_functions)
            return type.__new__(meta, classname, supers, classdict)

    return DecorateMetaClass
