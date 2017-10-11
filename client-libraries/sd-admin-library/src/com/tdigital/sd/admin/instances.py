'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''


class Instances(object):
    """Administration of instances

    This class provides methods to create, get, and delete an instance as well
    as to find a list of instances under certain filter criteria
    """

    # Relative path to the instances resource where class_name is a parameter to be replaced
    PATH_INSTANCES_TEMPLATE = 'classes/{class_name}/instances'
    # Relative path to a single instance resource where class_name and instance are parameters to be replaced
    PATH_INSTANCE_TEMPLATE = 'classes/{class_name}/instances/{instance_id}'

    def __init__(self, client):
        """Constructor

        Stores a HTTP client reference to access the service directory

        :param client HTTP client to access service directory (Mandatory)
                      It is an instance of com.tdigital.sd.admin.client.Client class
        """

        self.client = client

    def create(self, class_name, version, environment, uri, **attributes):
        """Create an instance

        Create a new instance for class "class_name"

        :param class_name class associated to the instance (Mandatory)
        :param version class version for this instance (Mandatory)
        :param environment environment this instance (optional)
        :param url URL where the instance is available (Mandatory)
        :param kwargs optional attributes dict for the endpoint
        :return Dictionary with the instance created
        """
        # when attributes is empty dict we should not send attributes in body
        body = dict(class_name=class_name, version=version, environment=environment,
                      uri=uri)
        if len(attributes) > 0:
            body['attributes'] = attributes
        response = self.client.post(
            Instances.PATH_INSTANCES_TEMPLATE.format(class_name=class_name),
            body=body)
        return response

    def find(self, class_name, **kwargs):
        """Find instances

        Get a list of instances for class "class_name" and other filter criteria

        :param class_name class associated to the instance (Mandatory)
        :param **kwargs Dictionary of optional parameters to filter the search of instances (Optional)
        :return Dictionary with the array of instances matching the query
        """

        response = self.client.get(Instances.PATH_INSTANCES_TEMPLATE.format(class_name=class_name), params=kwargs)
        return response

    def get(self, class_name, instance_id):
        """Get instance

        Get an instance identified by "instance_id" and associated to class "class_name"

        :param class_name class associated to the instance (Mandatory)
        :param instance_id instance UUID (Mandatory)
        :return Dictionary with the instance info matching the query
        """

        response = self.client.get(Instances.PATH_INSTANCE_TEMPLATE.format(class_name=class_name,
                                                                           instance_id=instance_id))
        return response

    def update(self, class_name, instance_id, params=None, attributes=None):
        """Update instance

        Update an instance, identified by "class_name" and "instance_id". It permits partial updates (maintaining
        constant the rest of the instance info). The attributes to update are included in kwargs.
        To support a partial update, the first step is to get the instance info because the service directory
        only provides full update.

        :param class_name class unique identifier (Mandatory)
        :param instance_id instance UUID (Mandatory)
        :param params instance attributes to be modified
        :param attributes attributes keys-values to be updated
        :return Dictionary with the class info matching the query
        """

        instance = self.get(class_name, instance_id)
        if params:
            instance.update(params)
        if attributes:
            instance['attributes'] = attributes
        response = self.client.put(Instances.PATH_INSTANCE_TEMPLATE.format(class_name=class_name,
                                                                           instance_id=instance_id), body=instance)
        return response

    def delete(self, class_name, instance_id):
        """Delete an instance

        Delete an instance identified by "instance_id" and associated to class "class_name"

        :param class_name class associated to the instance (Mandatory)
        :param instance_id instance UUID (Mandatory)
        """
        return self.client.delete(Instances.PATH_INSTANCE_TEMPLATE.format(class_name=class_name,
                                                                          instance_id=instance_id))
