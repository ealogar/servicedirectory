'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
import functools
from time import sleep
import logging


def retry(backoff=1, delay=50, max_retries=1, exceptions=(Exception,), logger_name=__name__):
    """
    Decorator function to call the decorated method again if some exception is raised.
    When a exception of the type is caught, a variable sleep is performed before retrying
    again the operation until a maximun number.
    Any other exception or valid return value will make the decorator to return them.

    :param backoff Multiply dealy by this factor every raised Error
    :param delay the time to sleep (in miliseconds) when a fail occurs
    :param max_retries the maximun number of times to retry the operation
    :param exceptions A tuple of Exception to catch for retry the operation
    """
    # get logger
    logger = logging.getLogger(logger_name)

    # Decorator defined inside to receive input params and keep callable with arguments
    def apply_decorator(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            num_retries = 0
            op_delay = delay
            # Retry the function until max
            while num_retries < max_retries:
                try:
                    rv = f(*args, **kwargs)
                    return rv
                except exceptions as e:
                    num_retries += 1
                    logger.warning("Operation failed, trying another time [%s of %s]", num_retries,
                                                                                       max_retries)
                    sleep(op_delay / 1000.0)
                    op_delay = (backoff + num_retries) * delay
                except Exception as e:
                    logger.error("Operation Problem: %s", str(e))
                    raise e

            logger.error("Operation failed permanently after %s retries", max_retries)
            raise Exception("Internal server error. Try again later")
        return wrapper
    return apply_decorator


def log_function_decorator(log_method='debug', logger_name=__name__):
    """
    Log input parameters and method name before the function is called.

    :param log_method the logger method to use (debug, info, warning, error)
    :param logger the logger to be used, if not defined a default will be used instead
    """
    # get logger
    logger = logging.getLogger(logger_name)

    def apply_decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            log_function = getattr(logger, log_method, 'debug')

            # Construct the log message dynamically depending on the args and kwargs
            base_msg = 'Calling ({0}.{1})'.format(args[0].__class__.__name__, f.__name__)
            if len(args) == 1 and len(kwargs) == 0:
                post_msg = ' without arguments'
            elif len(args) > 1 and len(kwargs) == 0:
                post_msg = 'with args {0} and no extra kw args'.format(args[1:])
            elif len(args) == 1 and len(kwargs) > 0:
                post_msg = ' with kw args {0}'.format(kwargs)
            else:
                post_msg = ' with args {0} and kw args {1}'.format(args[1:], kwargs)

            log_function('{0}{1}'.format(base_msg, post_msg))
            return f(*args, **kwargs)
        return wrapper

    return apply_decorator
