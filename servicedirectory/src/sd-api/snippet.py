from functools import wraps

def generate_fixed_length_param(param):
    """
    Generate a fixed length param if the elements matches the expression
    [<type>_WITH_LENGTH_<length>] in lettuce. E.g.: [STRING_WITH_LENGTH_15]
    :param param: Lettuce param
    :return param with the desired length
    """
    try:
        if "_WITH_LENGTH_" in param:
            if "_ARRAY_WITH_LENGTH_" in param:
                seeds = {'STRING': 'a', 'INTEGER': 1}
                seed, length = param[1:-1].split("_ARRAY_WITH_LENGTH_")
                param = list(seeds[seed] for x in xrange(int(length)))
            elif "JSON_WITH_LENGTH_" in param:
                length = int(param[1:-1].split("JSON_WITH_LENGTH_")[1])
                param = dict((str(x), str(x)) for x in xrange(length))
            else:
                seeds = {'STRING': 'a', 'INTEGER': 1}
                seed, length = param[1:-1].split("_WITH_LENGTH_")
                param = seeds[seed] * int(length)
    finally:
        return param

def generate_fixed_length_params(data):
    """
    Generate a fixed length data for the elements that match the expression
    [<type>_WITH_LENGTH_<length>] in lettuce. E.g.: [STRING_WITH_LENTGH_15]
    :param data: Lettuce step hash entry
    :return data with the desired params with the desired length
    """
    try:
        for item in data.keys():
            data[item] = generate_fixed_length_param(data[item])
    finally:
        return data

def auto_expand(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        args = map(generate_fixed_length_param, args)
        kwargs.update(generate_fixed_length_params(kwargs))
            
        return f(*args, **kwargs)
    return wrapper



@auto_expand
def prueba(arg1, arg2, arg3):
    print 'arg1', arg1
    print 'arg2', arg2
    print 'arg3', arg3


if __name__ == '__main__':
    prueba('[STRING_WITH_LENGTH_5]', arg3 = 'standard chain', arg2 = '[STRING_WITH_LENGTH_10]')

