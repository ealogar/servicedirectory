'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''


def convert_string_to_bool(input_str, allow_flex_bolean=False):
    if allow_flex_bolean:
        input_str = input_str.lower()
        allowed_true_value = ('true', 't', '1', 'on')
        allowed_false_value = ('false', 'f', '0', 'off')
    else:
        allowed_true_value = ('true', )
        allowed_false_value = ('false', )
    # note that t, 1 and on have been removed
    if input_str in allowed_true_value:
        return True
    if input_str in allowed_false_value:
        return False
    return None


def convert_string_to_int(input_str):
    try:
        return int(input_str)
    except ValueError:
        return None


def convert_string_to_float(input_str):
    try:
        if convert_string_to_int(input_str) is None:
            return float(input_str)
        else:
            return None
    except ValueError:
        return None


def convert_str_to_type(input_str, primitive_type):
    """
    Utility function to convert a string to the primitive_type indicated by params.
    if conversion is not possible, None will be returned

    :param input_str the string to convert
    :param primitive_type the type of the primitive to transform the input

    :return the converted string to the primitive or None if not possible
    """
    if primitive_type == bool:
        return convert_string_to_bool(input_str)
    elif primitive_type == int:
        return convert_string_to_int(input_str)
    elif primitive_type == float:
        return convert_string_to_float(input_str)
    elif primitive_type in (str, unicode):
        return input_str
    else:
        return None


def pretty_type(obj):
    if type(obj) == bool:
        return 'boolean'
    elif type(obj) == int:
        return 'integer'
    elif type(obj) == float:
        return 'number'
    elif type(obj) in (str, unicode):
        return 'string'
    else:
        return type(obj).__name__
