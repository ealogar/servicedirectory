'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from com.tdigital.sd.admin.exceptions import NotFoundException


class Bindings(object):
    """Administration of rules for service class and origins.

    This class provides methods to create, get, update, and delete an origin rule as well
    as to find the list of client rules for a given service class.

    An origin will be the identifier of the client who wants to set the rules; it may exist or no
    inside Service directory.
    """

    # Relative path to all the client rules associated to an class where class_name is a parameter to be replaced
    PATH_BINDINGS = 'bindings'
    # Relative path to the client rules resource where class_name and origin are parameters to be replaced
    PATH_BINDINGS_TEMPLATE = 'bindings/{binding_id}'

    def __init__(self, client):
        """Constructor

        Stores a HTTP client reference to access the service directory

        :param client HTTP client to access service directory (Mandatory)
                      It is an instance of com.tdigital.sd.admin.client.Client class
        """

        self.client = client

    def create(self, class_name, origin, rules):
        """Create the client rules

        Create the client rules for service class "class_name" and client "origin".

        :param class_name class associated to the client rules (Mandatory)
        :param origin Name of the client owner of these rules (Mandatory)
        :param rules Dictionary with the rules for the client (Mandatory)
        :return Dictionary with the rules created for this client
        """
        # The rule does not exist
        rules.update({'class_name': class_name, 'origin': origin})
        response = self.client.post(Bindings.PATH_BINDINGS, body=rules)
        return response

    def find(self, **kwargs):
        """Find rules

        Get a list of client rules for class "class_name" and other filter criteria

        :param class_name class associated to the client rules (Mandatory)
        :param **kwargs Dictionary of optional parameters to filter the search of client rules (Optional)
                        only class_name and origin are valid filter criteria.
        :return Dictionary with the array of client rules matching the query
        """
        response = self.client.get(Bindings.PATH_BINDINGS, params=kwargs)
        return response

    def get(self, class_name, origin):
        """Get rules for origin and service class indicated

        Get the client rules associated to class "class_name" and client "origin"

        :param class_name class associated to the rules (Mandatory)
        :param origin Name (Mandatory)
        :return Dictionary with the client rules for this class
        """
        search_query = {'class_name': class_name, 'origin': origin}
        response = self.client.get(Bindings.PATH_BINDINGS, params=search_query)
        if len(response) >= 1:
            return response[0]
        else:
            raise NotFoundException('class {0} origin {1}'.format(class_name, origin))

    def update(self, class_name, origin, rules):
        """Update the client rules

        Update the client rules for service class "class_name" and client "origin". It also checks that
        the client has already defined rules. This operation does not permit a partial update.

        :param class_name class associated to the client rules (Mandatory)
        :param origin Name of the client owner of these rules (Mandatory)
        :param rules Dictionary with the rules for the client (Mandatory)
        :return Dictionary with the rules created for this client
        """

        old_rules = self.get(class_name, origin)  # not found raised in client
        rules.update({'class_name': class_name, 'origin': origin})  # Yes, we know is mutable...
        return self.client.put(
            Bindings.PATH_BINDINGS_TEMPLATE.format(binding_id=old_rules['id']), body=rules)

    def delete(self, class_name, origin):
        """Delete client rules

        Delete the client rules identified by "origin" and associated to class "class_name"

        :param class_name class associated to the client rules (Mandatory)
        :param origin Name of the client owner of these rules (Mandatory)
        """
        old_rules = self.get(class_name, origin)
        return self.client.delete(Bindings.PATH_BINDINGS_TEMPLATE.format(binding_id=old_rules['id']))
