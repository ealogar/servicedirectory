'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from commons.exceptions import NotFoundException


class NotBindingDefinedException(NotFoundException):
    """
    Especial case of NotFoundException to deal with bind_instances operation
    when no binding is defined for the context params given (origin or default)
    """
    _unica_code = 'SVC2002'

    def __init__(self, class_name, origin):
        # fulfill _details
        resource_name = '{0}-{1}'.format(class_name, origin)
        super(NotBindingDefinedException, self).__init__(resource_name)


class DeletedInstanceException(NotFoundException):
    """
    Especial case of NotFoundException to deal with bind_instances operation
    when binding_instance recovered has been deleted
    """
    _unica_code = 'SVC2003'


class NotMatchingRuleException(NotFoundException):
    """
    Especial case of NotFoundException to be raised when no rule matched the
    input context params given
    """
    _unica_code = 'SVC1006'

    def __init__(self, class_name, origin):
        # fulfill _details
        resource_name = 'binding-{0}-{1}'.format(class_name, origin)
        super(NotMatchingRuleException, self).__init__(resource_name)


class NotBindingInstanceException(NotMatchingRuleException):
    """
    Especial case of NotFoundException to be raised when no rule matched the
    input context params given
    """
    _unica_code = 'SVC1006'
