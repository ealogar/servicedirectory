# -*- coding: utf-8 -*-
'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from lettuce import world
import requests
import re
from string import Template
import bson
import json


class RestUtils(object):

    def prepare_plain_data(self, data):
        try:
            data = self.generate_fixed_lenght_params(data)
            data = self.remove_missing_params(data)
            data = self.infere_datatypes(data)
            return data
        except:
            return None

    def prepare_data(self, step, hash_index):
        try:
            data = step.hashes[hash_index]
            return self.prepare_plain_data(data)
        except:
            return None

    def remove_missing_params(self, data):
        """
        Removes al the data elements tagged with the text [MISSING_PARAM] in lettuce
        :param data: Lettuce step hash entry
        """
        try:
            for item in data.keys():
                        if "[MISSING_PARAM]" in data[item]:
                            del(data[item])
        finally:
            return data

    def generate_fixed_lenght_params(self, data):
        """
        Generate a fixed length data for elements tagged with the text [LENGHT] in lettuce
        :param data: Lettuce step hash entry
        """
        try:
            seeds = {'STRING': 'a', 'INTEGER': 1}
            for item in data.keys():
                if "_WITH_LENGTH_" in data[item]:
                    seed, length = data[item][1:len(data[item]) - 1].split("_WITH_LENGTH_")
                    data[item] = seeds[seed] * int(length)
        finally:
            return data

    def infere_datatypes(self, data):
        """
        Transformes data from string to primitive type
        :param data: Data to be transformed
        """

        """ Separate the process of lists, dicts and plain items"""

        try:

            if isinstance(data, dict):
                for item in data:
                    try:
                        data[item] = int(data[item])
                    except:
                        try:
                            if "[TRUE]" in data[item]:
                                data[item] = True
                            if "[FALSE]" in data[item]:
                                data[item] = False
                            else:
                                data[item] = float(data[item])
                        except:
                            continue

            if isinstance(data, list):
                for item in range(1, len(data)):
                    try:
                        data[item] = int(data[item])
                    except:
                        try:
                            if "[TRUE]" in data[item]:
                                data[item] = True
                            if "[FALSE]" in data[item]:
                                data[item] = False
                            else:
                                data[item] = float(data[item])
                        except:
                            continue

            if not isinstance(data, list) and not isinstance(data, dict):
                """ Assumption of single item """
                try:
                    data = int(data)
                except:
                        try:
                            if "[TRUE]" in data:
                                data = True
                            if "[FALSE]" in data:
                                data = False
                            else:
                                data = float(data)
                        except:
                            return data
        finally:
            return data

    def generate_attributes(self, attributes_keys, attributes_values):
        """
        Generates the instances attributes dictionary from a list of keys and values in the lettuce step
        :param key: Attributes keys
        :param data: Attributes values
        """
        attributes = {}

        try:
            if "[MALFORMED]" in attributes_keys:
                attributes = [""]
                return attributes

            if "ARRAY_WITH_ITEMS_" in attributes_keys:
                length = attributes_keys[1:len(attributes_keys) - 1].split("_WITH_ITEMS_")[1]
                fixed_attributes = {}
                for value in range(0, int(length)):
                    fixed_attributes[str(value)] = str(value)
                return fixed_attributes
            else:
                try:
                    attributes = dict(zip(attributes_keys.split(","),\
                                        attributes_values.split(",")))
                    return self.infere_datatypes(attributes)
                except:
                    #attributes are a single value that has been infered. Just zip it
                    attributes = dict(zip([attributes_keys], [attributes_values]))
                    return self.infere_datatypes(attributes)
        except:
            return attributes

    def request_the_resource(self, step, url_template, params_index=-1, headers_index=-1):
        """
        Send a GET request with params to the URL provided, and store the
        result in the world (status code and JSON received, if any).
        :param step: Current Lettuce step.
        :param url_template: Template of the URL where to send the request.
        :param headers_index:  Index of the headers information within the step.
        :param params_index: Index of the params information within the step.
        """

        """Get the URL with values from the template."""
        url = self._get_url_with_values(url_template)

        """Get the params to be sent, if any."""
        if params_index >= 0:
            params = self.prepare_data(step, int(params_index))
            print 'params: ', params
        else:
            params = None

        """Get the headers to be sent, if any."""
        if headers_index >= 0:
            headers = self.prepare_data(step, int(headers_index))
            print 'headers: ', headers
        else:
            headers = None

        """Check if a specific user has been defined for the request
        If not, get the authentication tuple from the properties."""

        if world.request_user is None:
            auth = None

        else:
            auth = (world.request_user, world.request_password)

        """Send the request."""
        try:
            res = requests.get(url, params=params, auth=auth, headers=headers)
            print 'Response: ', res, res.status_code
        except:
            assert False, "Django server connection error. URL: %s" % url

        """Store response values for future assertions"""
        world.status_code = res.status_code
        try:
            world.json = res.json()
        except:
            world.json = None

    def send_to_url_the_data(self, step, url_template, data, provided_header={}):
        """
        Send a POST request with the data provided to the URL provided, and store
        the result in the world (status code and JSON received, if any).
        :param step: Current Lettuce step.
        :param url_template: Template of the URL where to send the request.
        :param data: Content of the request to be sent.
        """

        data = self.prepare_plain_data(data)

        """Get the URL with values from the template."""
        url = self._get_url_with_values(url_template)

        """Check if a specific user has been defined for the request
        If not, get the authentication tuple from the properties."""

        if world.request_user is None:
            auth = None

        else:
            auth = (world.request_user, world.request_password)

        """Define content and content type based on data content"""
        """Set json content type in the headers only if needed."""

        headers = provided_header
        tunned_data = json.dumps(data)

        if data != "UNSTRUCTURED_DATA":
            headers.update({'Content-Type': 'application/json'})

        if data == "UNSTRUCTURED_DATA":
            headers.update({'Content-Type': 'text/plain'})

        if data == "MALFORMED_DATA":
            tunned_data = '"{,}"'

        elif data == "REPEATED_KEY":
            tunned_data = '{"version": "v1.0","uri": "repeated_attributes",\
            "attributes": {"key_repeated": "test","key_repeated": "test"}}'

        """Send the request"""
        try:
            print 'requests.post(', url, tunned_data, ')'
            res = requests.post(url, tunned_data, auth=auth, headers=headers)
            print res, res.json()
        except:
            assert False, "Django server connection error. URL: %s" % url

        """Store response values for future assertions"""
        world.status_code = res.status_code
        try:
            world.location = res.headers["Location"]
        except:
            """ If resource is note created the header will not be sent """
            world.location = None
        try:
            world.correlator = res.headers["Unica-Correlator"]
        except:
            """ If unica correlator can not be generated (i.e. wrong settings) it will not be returned """
            world.correlator = None
        try:
            world.json = res.json()
        except:
            world.json = None

    def put_in_url_the_data(self, step, url_template, data):
        """
        Send a PUT request with the data provided to the URL provided, and store
        the result in the world (status code and JSON received, if any).
        :param step: Current Lettuce step.
        :param url_template: Template of the URL where to send the request.
        :param data: Content of the request to be sent.
        """

        data = self.prepare_plain_data(data)

        """Get the URL with values from the template."""
        url = self._get_url_with_values(url_template)

        """Check if a specific user has been defined for the request
        If not, get the authentication tuple from the properties."""

        if world.request_user is None:
            auth = None

        else:
            auth = (world.request_user, world.request_password)

        """Define content and content type based on data content"""
        """Set json content type in the headers only if needed."""

        headers = {}
        tunned_data = json.dumps(data)

        if data != "UNSTRUCTURED_DATA":
            headers.update({'Content-Type': 'application/json'})

        if data == "UNSTRUCTURED_DATA":
            headers.update({'Content-Type': 'text/plain'})

        if data == "MALFORMED_DATA":
            tunned_data = '"{,}"'

        elif data == "REPEATED_KEY":
            tunned_data = '{"version": "v1.0","url": "repeated_attributes",\
            "attributes": {"key_repeated": "test","key_repeated": "test"}}'

        """Send the request"""
        try:
            res = requests.put(url, tunned_data, auth=auth, headers=headers)
        except:
            assert False, "Django server connection error. URL: %s" % url

        """Store response values for future assertions"""
        world.status_code = res.status_code
        try:
            world.location = res.headers["Location"]
        except:
            """ If resource is note created the header will not be sent """
            world.location = None
        try:
            world.correlator = res.headers["Unica-Correlator"]
        except:
            """ If unica correlator can not be generated (i.e. wrong settings) it will not be returned """
            world.correlator = None
        try:
            world.json = res.json()
        except:
            world.json = None

    def delete_url(self, step, url_template):
        """
        Send a DELETE request to the URL provided, and store the result in the
        world (status code and JSON received, if any).
        :param step: Current Lettuce step.
        :param url_template: Template of the URL where to send the request.
        """

        """Get the URL with values from the template."""
        url = self._get_url_with_values(url_template)

        """Check if a specific user has been defined for the request
        If not, get the authentication tuple from the properties."""

        if world.request_user is None:
            auth = None
        else:
            auth = (world.request_user, world.request_password)

        """Send the request"""

        try:
            res = requests.delete(url, auth=auth)
        except:
            assert False, "Django server connection error. URL: %s" % url

        """Store response values for future assertions"""
        world.status_code = res.status_code
        try:
            world.json = res.json()
        except:
            world.json = None

    def get_a_success_response_of_type_with_location(self, step, status_code, location_index):
        """
        Check that the result of the previous request has the type and the location
        provided.
        :param step: Current Lettuce step.
        :param status_code: Expected status code of the response.
        :param location_index: Index of the expected location within the step.
        """
        expected_status_code = int(status_code)
        location_template = step.hashes[int(location_index)]["location"]

        """Get the URL with values from the template."""
        expected_location = self._get_url_with_values(location_template)

        """Check the response"""
        assert expected_status_code == world.status_code, \
            "Unexpected type received. Expected: %d. Received: %d." \
            % (expected_status_code, world.status_code)

        location_regex = re.compile(expected_location)
        match_result = location_regex.match(world.location)
        assert match_result, \
            "The location does not match expression %s. Received: %s." \
            % (expected_location, world.location)

        if (world.config["django"]["instances_url"]) in world.location:
            """If the instance ID was captured, store it as an ObjectId"""
            if match_result.lastindex == 1:
                object_id = bson.ObjectId(match_result.group(1))
                world.instance[world.config["keys"]["id"]] = object_id

    def get_a_success_response_of_type_with_error_code_with_location(self, step, status_code, error_code, location_index):
        """
        Check that the result of the previous request has the type and the location
        provided.
        :param step: Current Lettuce step.
        :param status_code: Expected status code of the response.
        :param location_index: Index of the expected location within the step.
        """
        expected_status_code = int(status_code)
        expected_error_code = str(error_code)
        location_template = step.hashes[int(location_index)]["location"]

        """Get the URL with values from the template."""
        expected_location = self._get_url_with_values(location_template)

        """Check the response"""
        assert expected_status_code == world.status_code, \
            "Unexpected type received. Expected: %d. Received: %d." \
            % (expected_status_code, world.status_code)
        try:
            received_error_code = world.json[world.config["keys"]["error_code"]]
        except:
            assert False, "Error getting the error code from the JSON: %s" \
            % str(world.json)
        assert expected_error_code == received_error_code, \
            "Unexpected error code. Expected: %s. Received: %s." \
            % (expected_error_code, received_error_code)

        location_regex = re.compile(expected_location)
        match_result = location_regex.match(world.location)
        assert match_result, \
            "The location does not match expression %s. Received: %s." \
            % (expected_location, world.location)

        if (world.config["django"]["instances_url"]) in world.location:
            """If the instance ID was captured, store it as an ObjectId"""
            if match_result.lastindex == 1:
                object_id = bson.ObjectId(match_result.group(1))
                world.instance[world.config["keys"]["id"]] = object_id

    def get_a_success_response_of_type_with_resultset_of_size(self, step, status_code, size):
        """
        Check that the result of the previous request has the type provided and a
        content consisting in a JSON array with the number of elements provided.
        :param step: Current Lettuce step.
        :param type: Expected status code of the response.
        :param size: Expected number of elements in the JSON array.
        """
        expected_status_code = int(status_code)

        """Check the response"""
        assert expected_status_code == world.status_code, \
            "Unexpected type received. Expected: %d. Received: %d." \
            % (expected_status_code, world.status_code)
        try:
            resultset_size = len(world.json)
        except:
            assert False, "Error checking the data in the JSON: %s" \
                % str(world.json)
        assert resultset_size == int(size), \
            "Unexpected result set size. Expected: %d. Received: %d." \
            % (int(size), resultset_size)

    def get_a_success_response_of_type(self, step, status_code):
        """
        Check that the response of the previous request has the type provided.
        :param step: Current Lettuce step.
        :param type: Expected status code of the response.
        """
        expected_status_code = int(status_code)

        """Check the response"""
        assert expected_status_code == world.status_code, \
            "Unexpected type received. Expected: %d. Received: %d." \
            % (expected_status_code, world.status_code)

    def get_an_error_response_of_type_with_error_code(self, step, status_code, error_code):
        """
        Check that the result of the previous request has the type provided and a
        content consisting in a JSON element with the error code provided.
        :param step: Current Lettuce step.
        :param status_code: Expected status code of the response.
        :param error_code: Expected error code in the JSON element.
        """
        expected_status_code = int(status_code)
        expected_error_code = str(error_code)

        """Check the response"""
        assert expected_status_code == world.status_code, \
            "Unexpected response type. Expected: %d. Received: %d." \
            % (expected_status_code, world.status_code)
        try:
            received_error_code = world.json[world.config["keys"]["error_code"]]
        except:
            assert False, "Error getting the error code from the JSON: %s" \
            % str(world.json)
        assert expected_error_code == received_error_code, \
            "Unexpected error code. Expected: %s. Received: %s." \
            % (expected_error_code, received_error_code)

    def get_an_error_response_message(self, step, error_message):
        """
        Check that the result of the previous request has the error message provided.
        :param step: Current Lettuce step.
        :param error_message: Expected error message of the response.
        """
        expected_message = error_message

        try:
            received_error_message = world.json[world.config["keys"]["error_text"]]
        except:
            assert False, "Error getting the error message from the JSON: %s" \
            % str(world.json)
        assert re.search(expected_message, received_error_message), \
            "Unexpected error message. Expected: %s. Received: %s." \
            % (expected_message, received_error_message)

    def _get_url_with_values(self, url_template):
        """
        Build a URL with the right values in the placeholders of the template
        provided.
        :param url_template: URL template to set the corresponding values.
        :return The URL built
        """

        if "$api_name" in url_template:
            old_api_name = world.old_capability[world.config["keys"]["api_name"]]
        else:
            old_api_name = None
        if "$class_name" in url_template:
            old_class_name = world.old_class[world.config["keys"]["class_name"]]
        else:
            old_class_name = None
        if "$endpoint_id" in url_template:
            old_endpoint = world.old_endpoint[world.config["keys"]["id"]]
        else:
            old_endpoint = None
        if "$instance_id" in url_template:
            old_instance = world.old_instance[world.config["keys"]["id"]]
        else:
            old_instance = None
        if "$binding_id" in url_template:
            old_binding_id = world.old_binding_id
        else:
            old_binding_id = None
        if "$api_client_name" in url_template:
            old_client_name = world.published_rules[world.config["keys"]["api_client_name"]]
        else:
            old_client_name = None

        try:
            if "$base_api_url" in url_template and world.config["ha"]["enabled"]:
                frontend_ip = world.config["ha"]["frontend_balancer"]
                base_api_url = world.config["django"]["base_api_url"].replace('127.0.0.1', frontend_ip)
            else:
                base_api_url = world.config["django"]["base_api_url"]
        except:
            base_api_url = world.config["django"]["base_api_url"]

        temp = Template(url_template)
        return temp.safe_substitute(base_api_url=base_api_url,
            apis_url=world.config["django"]["apis_url"],
            classes_url=world.config["django"]["classes_url"],
            bind_instances_url=world.config["django"]["bind_instances_url"],
            bindings_url=world.config["django"]["bindings_url"],
            api_name=old_api_name,
            class_name=old_class_name,
            users_url=world.config["django"]["users_url"],
            endpoints_url=world.config["django"]["endpoints_url"],
            instances_url=world.config["django"]["instances_url"],
            endpoint_id=old_endpoint,
            instance_id=old_instance,
            binding_id=old_binding_id,
            api_client_name=old_client_name,
            request_context_rules_url=world.config["django"]["request_context_rules_url"],
            binding_rules=world.config["django"]["binding_rules"])
