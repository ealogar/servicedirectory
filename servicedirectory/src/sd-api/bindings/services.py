'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
import logging
from pymongo.errors import DuplicateKeyError
from bindings.exceptions import NotMatchingRuleException, DeletedInstanceException, NotBindingDefinedException,\
    NotBindingInstanceException

from commons.exceptions import GenericServiceError, NotFoundException, \
    UnsupportedParameterValueException, MissingMandatoryParameterException
from commons.services import BaseService, return_obj_or_raise_not_found
from classes.daos import ServiceClassDao, ServiceInstanceDao
from bindings.daos import BindingDao
from commons.utils import convert_str_to_type, pretty_type
import re


logger = logging.getLogger(__name__)


class BindingService(BaseService):
    """
    Service to handle Bindings objects with mongodb and provide
    all business logic needed to views layer
    """

    def __init__(self):
        self.binding_dao = BindingDao()
        self.class_dao = ServiceClassDao()
        self.instance_dao = ServiceInstanceDao()

    @return_obj_or_raise_not_found
    def get_binding_by_id(self, binding_id):
        return self.binding_dao.find(binding_id)

    def get_all_bindings(self, query_params):
        return self.binding_dao.find_bindings(query_params)

    def create_binding(self, binding):
        if not self.class_dao.find(binding['class_name']):
            raise NotFoundException(binding['class_name'])
        try:
            self.check_binding_rules_in_class(binding)
            return self.binding_dao.create(binding)
        except DuplicateKeyError:
            raise UnsupportedParameterValueException('{0}-{1}'.format(binding['class_name'], binding['origin']),
                                                     'non-duplicated-origin')

    def check_binding_rules_in_class(self, binding):
        for binding_rule in binding['binding_rules']:
            for binding_instance in binding_rule['bindings']:
                if not self.instance_dao.find_by_class_name_and_id(binding['class_name'], binding_instance):
                    raise UnsupportedParameterValueException(
                            binding_instance, "instances of {0}".format(binding['class_name']))

    def update_binding(self, binding):
        if not self.class_dao.find(binding['class_name']):
            raise NotFoundException(binding['class_name'])
        # if not binding is found, not found is already launched in serializers
        try:
            self.check_binding_rules_in_class(binding)
            if self.binding_dao.update_binding(binding):
                return binding
            else:
                raise GenericServiceError('The binding update process failed.')
        except DuplicateKeyError:
            raise UnsupportedParameterValueException('{0}-{1}'.format(binding['class_name'], binding['origin']),
                                                     'non-duplicated-origin')

    def delete_binding(self, binding_id):
        if not self.binding_dao.delete(binding_id,):
            raise GenericServiceError('The binding delete process failed.')

    def get_binding_instance(self, params):
        try:
            class_name = params.pop('class_name')
        except KeyError:
            raise MissingMandatoryParameterException('class_name')

        class_ = self.class_dao.find(class_name)
        if not class_:
            raise NotFoundException(class_name)

        origin = params.get('origin', 'default')
        binding = self.binding_dao.find_by_class_and_origin(class_name, origin)
        if binding is None:  # when rules are null in database
            rules = ()
        else:
            rules = binding['binding_rules']

        # perform the binding_instance operation
        if rules:
            binding_instances = self.get_binding_instances_by_rules(rules, params)
            if binding_instances is None:
                raise NotMatchingRuleException(class_name, origin)
            else:
                # Although we only return one binding_instance, in future this can deal
                # with several bindings and return the first binding alive
                if len(binding_instances) == 0:
                    raise NotBindingInstanceException(class_name, origin)
                binding_instance = self.instance_dao.find(binding_instances[0])
                if binding_instance:
                    return binding_instance
                else:
                    raise DeletedInstanceException(binding_instances[0])
        else:
            # No rules defined for the search
            raise NotBindingDefinedException(class_name, origin)

    def get_binding_instances_by_rules(self, rules, context):
        """
        Performs an ordered search over rules to return a tuple with the binding_instances and
        the input_key_param that first match with the context specified.

        :param rules and ordered array of rules for class_origins, defining also
                     the binding_instances
        :param context The request query parameters to be applied as input of the rules

        :return the (instances, keys) that first match with the rules
                If any rule is matched, ((), ()) will be returned
                If no rules for search are found, None will be returned
        """
        # Apply rules by priority
        for binding_rule in rules:
            # Check rule matches with context params
            matched_rule = True
            for rule in binding_rule['group_rules']:
                if not self.execute_rule(rule, context):
                    matched_rule = False
                    break
            if matched_rule:
                # rule matched, return bindings and keys
                return binding_rule['bindings']

        # No binding_rules found at all
        return None

    def execute_rule(self, rule, context):
        """
        Check if rule applied over context param is executed,
        that means the rule operand applied on the input param
        of context for the rule value is matched:
               input operand value is True
        :param rule a dict with operand, input_context_param and value
        :param context a dict with input context params value

        :return True if the rule can be executed for the context
        """
        try:

            left_operand = context[rule['input_context_param']]
            right_operand = rule['value']
            if rule['operation'] == 'eq':
                left_operand = convert_str_to_type(left_operand, type(right_operand[0]))
                return left_operand == right_operand[0]
            elif rule['operation'] == 'regex':
                pattern = re.compile(right_operand[0])
                return pattern.match(left_operand)
            elif rule['operation'] == 'range':
                if type(right_operand[0]) != type(right_operand[1]):
                    logger.error("Bad rule definition for range, min and max must be of same type")
                    raise GenericServiceError("Range rule defined is invalid")
                else:
                    left_operand_c = convert_str_to_type(left_operand, type(right_operand[0]))
                    if left_operand_c is None:
                        raise UnsupportedParameterValueException(left_operand, pretty_type(right_operand[0]))
                    return left_operand_c >= right_operand[0] and left_operand_c <= right_operand[1]
            elif rule['operation'] == 'in':
                left_operand_c = convert_str_to_type(left_operand, type(right_operand[0]))
                if left_operand_c is None:
                    raise UnsupportedParameterValueException(left_operand, pretty_type(right_operand[0]))
                return left_operand_c in right_operand
            else:
                msg = "Unsupported operand for rule {0}".format(rule['operation'])
                logger.error(msg)
                raise GenericServiceError(msg)

        except (AttributeError, KeyError) as e:
            logger.debug(str(e))

        return False
