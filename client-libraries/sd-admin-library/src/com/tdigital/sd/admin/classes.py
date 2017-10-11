'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''


class Classes(object):
    """Administration of classes

    This class provides methods to create, get, and delete an class as well
    as to find a list of classes under certain filter criteria
    """

    # Relative path to the classes resource
    PATH_CLASSES = 'classes'
    # Relative path to a single class resource where class_name is a parameter to be replaced
    PATH_CLASS_TEMPLATE = 'classes/{class_name}'

    def __init__(self, client):
        """Constructor

        Stores a HTTP client reference to access the service directory

        :param client HTTP client to access service directory (Mandatory)
                      It is an instance of com.tdigital.sd.admin.client.Client class
        """

        self.client = client

    def create(self, class_name, default_version, description):
        """Create an class

        Create a new class

        :param class_name class name (unique identifier for classes) (Mandatory)
        :param defaultversion Default class version when querying endpoints (Mandatory)
        :param description Description for the new class (Optional)
        :return Dictionary with the class created
        """

        body = {'class_name': class_name, 'default_version': default_version}
        if description is not None:
            body['description'] = description
        response = self.client.post(Classes.PATH_CLASSES, body=body)
        return response

    def find(self):
        """Find classes

        Get a list of classes with some filter criteria

        :param **kwargs Dictionary of optional parameters to filter the search of classes (Optional)
        :return Dictionary with the array of classes matching the query
        """

        response = self.client.get(Classes.PATH_CLASSES)
        return response

    def get(self, class_name):
        """Get class

        Get a class identified by "class_name"

        :param class_name class unique identifier (Mandatory)
        :return Dictionary with the class info matching the query
        """

        response = self.client.get(Classes.PATH_CLASS_TEMPLATE.format(class_name=class_name))
        return response

    def update(self, class_name, **kwargs):
        """Update class

        Update an class, identified by "class_name". It permits partial updates (maintaining constant the
        rest of the class info). The attributes to update are included in kwargs.
        To support a partial update, the first step is to get the class info because the service directory
        only provides full update.

        :param class_name class unique identifier (Mandatory)
        :param kwargs class attributes to be modified
        :return Dictionary with the class info matching the query
        """

        class_obj = self.get(class_name)
        class_obj.update(kwargs)
        response = self.client.post(Classes.PATH_CLASS_TEMPLATE.format(class_name=class_name), body=class_obj)
        return response

    def delete(self, class_name):
        """Delete an class

        Delete an class identified by "class_name"

        :param class_name class unique identifier (Mandatory)
        """

        return self.client.delete(Classes.PATH_CLASS_TEMPLATE.format(class_name=class_name))
