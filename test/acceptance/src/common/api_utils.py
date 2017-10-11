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
from rest_utils import RestUtils
import bson
import requests
import copy
import re

rest_utils = RestUtils()


class APIUtils(object):

    def generate_endpoint(self, data):
        """
        Generates the endpoint to be pusblished with the information provided in the step
        :param data: Master data to generate the endpoint
        """

        try:

            if "[REPEATED_KEY]" in data["attributes_keys"]:
                return "REPEATED_KEY"

            else:
                data = rest_utils.remove_missing_params(data)
                endpoint = rest_utils.generate_fixed_lenght_params(data)
                endpoint[world.config["keys"]["attributes"]] = rest_utils.generate_attributes(\
                data["attributes_keys"], \
                data["attributes_values"])

                del  endpoint["attributes_keys"]
                del  endpoint["attributes_values"]

        except:
            endpoint = rest_utils.remove_missing_params(data)

        rest_utils.infere_datatypes(endpoint)

        return endpoint

    def generate_instance(self, data):
        """
        Generates the instance to be published with the information provided in the step
        :param data: Master data to generate the instance
        """

        data = rest_utils.generate_fixed_lenght_params(data)

        try:

            if "[REPEATED_KEY]" in data["attributes_keys"]:
                return "REPEATED_KEY"

            else:
                instance = rest_utils.remove_missing_params(data)
                instance[world.config["keys"]["attributes"]] = rest_utils.generate_attributes(\
                data["attributes_keys"], \
                data["attributes_values"])

                del  instance["attributes_keys"]
                del  instance["attributes_values"]

        except:
            instance = rest_utils.remove_missing_params(data)

        rest_utils.infere_datatypes(instance)

        return instance

    def generate_binding(self, data):
        """
        Generates the binding to be pusblished with the information provided in the step
        :param data: Master data to generate the binding
        """

        """Remove missing params defined in test"""
        world.binding = rest_utils.remove_missing_params(data)

        """Add previously stored binding_rules"""
        world.binding[world.config["keys"]["binding_rules"]] = copy.copy(world.binding_rules)

        return  world.binding

    def send_to_url_the_capability_data(self, step, url, cap_index):
        """
        Send to the URL provided a JSON with the capability data provided, and
        keep in the world that data.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        :param cap_index: Index of the capability information within the step.
        """
        world.published_capability = step.hashes[int(cap_index)]

        """Special handling of the self-defined keyword [_ID]"""
        if world.config["keys"]["api_name"] in world.published_capability and \
            world.published_capability[world.config["keys"]["api_name"]].startswith("[_ID]"):
            """Set the api name in the _id mongo key instead of the api_name key"""
            world.published_capability[world.config["mongodb"]["_id"]] = \
                world.published_capability.pop(world.config["keys"]["api_name"])[5:]

        rest_utils.send_to_url_the_data(step, url, world.published_capability)

        """ After class publication add all the values not contained in published_capability for future validation """
        """ class_name can not be overwritten """
        try:
            for key in world.base_class.keys():
                if key not in world.published_capability:
                    world.published_capability[key] = world.base_class[key]
                world.published_capability["class_name"] = world.base_class["class_name"]
        except:
            pass

    def send_to_url_the_class_data(self, step, url, class_index, header={}):
        """
        Send to the URL provided a JSON with the class data provided, and
        keep in the world that data.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        :param class_index: Index of the capability information within the step.
        """

        try:
            world.published_class = step.hashes[int(class_index)]
        except:
            published_class_without_missing = rest_utils.remove_missing_params(step.hashes[int(class_index)])
            world.published_class = rest_utils.generate_fixed_lenght_params(published_class_without_missing)

        rest_utils.send_to_url_the_data(step, url, world.published_class, header)

        if world.status_code == 201:
            world.old_class = world.json

        """ After class publication add all the values not contained in published_capability for future validation """
        """ class_name can not be overwritten """
        try:
            for key in world.base_class.keys():
                if key not in world.published_class:
                    world.published_class[key] = world.base_class[key]
                world.published_class["class_name"] = world.base_class["class_name"]
        except:
            pass

    def send_to_url_the_endpoint_data(self, step, url, endpoint_index):
        """
        Send to the URL provided a JSON with the endpoint data provided, and
        keep in the world that data.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        :param endpoint_index: Index of the endpoint information within the step.
        """
        world.endpoint = self.generate_endpoint(step.hashes[int(endpoint_index)])

        rest_utils.send_to_url_the_data(step, url, world.endpoint, provided_header=None)

    def send_to_url_the_instance_data(self, step, url, instance_index):
        """
        Send to the URL provided a JSON with the instance data provided, and
        keep in the world that data.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        :param instance_index: Index of the instance information within the step.
        """
        world.instance = self.generate_instance(step.hashes[int(instance_index)])

        rest_utils.send_to_url_the_data(step, url, world.instance)

    def send_to_url_the_rule_data(self, step, url, rule_index):
        """
        Send to the URL provided a JSON with the rules data provided, and
        keep in the world that data.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        :param rule_index: Index of the rule information within the step.
        """
        world.binding = self.generate_binding(step.hashes[int(rule_index)])

        rest_utils.send_to_url_the_data(step, url, world.binding)

        """ Store a copy of the published binding for resource validation"""
        world.published_rules = copy.copy(world.binding)

        """Keep the id generated by the DB in world.old_binding_id too"""
        try:
            world.old_binding_id = world.json[world.config["keys"]["binding_id"]]
        except:
            """ Binding creation none completed will have empty json and id will be null """
            world.old_binding_id = None

        """ Reset world binding and binding_rules after publication of an origin"""
        world.binding = []
        world.binding_rules = []

    def send_to_url_the_user_data(self, step, url, user_index):
        """
        Send to the URL provided a JSON with the rules data provided, and
        keep in the world that data.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        :param user_index: Index of the user information within the step.
        """

        world.created_user = step.hashes[int(user_index)]

        for param in world.created_user.keys():
                if "[MISSING_PARAM]" in world.created_user[param]:
                    del(world.created_user[param])

        try:
            if step.hashes[int(user_index)]["classes"] == "":
                step.hashes[int(user_index)]["classes"] = []
            else:
                step.hashes[int(user_index)]["classes"] = step.hashes[int(user_index)]["classes"].split(",")
        except:
            pass

        try:
            if step.hashes[int(user_index)]["origins"] == "":
                step.hashes[int(user_index)]["origins"] = []
            else:
                step.hashes[int(user_index)]["origins"] = step.hashes[int(user_index)]["origins"].split(",")
        except:
            pass

        rest_utils.send_to_url_the_data(step, url, step.hashes[int(user_index)])

    def put_in_url_the_endpoint_data(self, step, url, endpoint_index):
        """
        Send to the URL provided a JSON with the endpoint data provided, and
        keep in the world that data.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        :param endpoint_index: Index of the endpoint data within the step.
        """
        world.endpoint = self.generate_endpoint(step.hashes[int(endpoint_index)])

        rest_utils.put_in_url_the_data(step, url, world.endpoint)

    def put_in_url_the_instance_data(self, step, url, instance_index):
        """
        Send to the URL provided a JSON with the instance data provided, and
        keep in the world that data.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        :param instance_index: Index of the instance data within the step.
        """
        world.instance = self.generate_instance(step.hashes[int(instance_index)])

        rest_utils.put_in_url_the_data(step, url, world.instance)

    def put_in_url_the_binding_data(self, step, url, binding_index):
        """
        Send to the URL provided a JSON with the instance data provided, and
        keep in the world that data.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        :param instance_index: Index of the instance data within the step.
        """

        world.binding = self.generate_binding(step.hashes[int(binding_index)])

        rest_utils.put_in_url_the_data(step, url, world.binding)

        """ Store a copy of the published binding for resource validation"""
        world.published_rules = copy.copy(world.binding)

        """Keep the id generated by the DB in world.old_binding_id too"""
        try:
            world.old_binding_id = world.json[world.config["keys"]["binding_id"]]
        except:
            """ Binding creation none completed will have empty json and id will be null """
            world.old_binding_id = None

        """ Reset world binding and binding_rules after publication of an origin"""
        world.binding = []
        world.binding_rules = []

    def a_capability_has_already_been_published_with_data(self, step, old_cap_index):
        """
        Publish through the API and keep in the world the capability data provided.
        :param step: Current Lettuce step.
        :param old_cap_index: Index of the endpoint data within the step.
        """

        world.old_capability = step.hashes[int(old_cap_index)]

        """Send the request to publish the capability using a URL template."""
        url_template = "$base_api_url/$apis_url"
        self.send_to_url_the_class_data(step, url_template, old_cap_index)

    def a_capability_has_not_already_been_published_with_data(self, step, old_cap_index):
        """
        Keep in the world the capability data provided without publishing it.
        :param step: Current Lettuce step.
        :param old_cap_index: Index of the endpoint data within the step.
        """
        world.old_capability = step.hashes[int(old_cap_index)]

    def a_class_has_already_been_published_with_data(self, step, old_class_index):
        """
        Publish through the API and keep in the world the class data provided.
        :param step: Current Lettuce step.
        :param old_class_index: Index of the instance data within the step.
        """

        url_template = "$base_api_url/$classes_url"
        class_name_template = step.hashes[int(old_class_index)][world.config["keys"]["class_name"]]
        rest_utils.request_the_resource(step, "".join([url_template, "/", class_name_template]))

        if (world.status_code == 404):
            world.old_class = step.hashes[int(old_class_index)]
            """Send the request to publish the capability using a URL template."""
            self.send_to_url_the_class_data(step, url_template, old_class_index, world.old_class)
        elif (world.status_code == 200):
            world.old_class = world.json
        else:
            print 'Non expected error code= ', world.status_code

    def a_class_has_not_already_been_published_with_data(self, step, old_class_index):
        """
        Keep in the world the class data provided without publishing it.
        :param step: Current Lettuce step.
        :param old_class_index: Index of the instance data within the step.
        """
        world.old_class = step.hashes[int(old_class_index)]

    def an_endpoint_has_already_been_published_with_data(self, step, old_endpoint_index):
        """
        Publish through the API and keep in the world the endpoint data provided.
        :param step: Current Lettuce step.
        :param old_endpoint_index: Index of the endpoint data within the step.
        """

        """Generate attributes if they are provided in key value format"""
        try:
            world.old_endpoint = step.hashes[int(old_endpoint_index)]
            world.old_endpoint[world.config["keys"]["attributes"]] = rest_utils.generate_attributes(\
                step.hashes[int(old_endpoint_index)]["attributes_keys"], \
                step.hashes[int(old_endpoint_index)]["attributes_values"])

            del  world.old_endpoint["attributes_keys"]
            del  world.old_endpoint["attributes_values"]

        except:
            world.old_endpoint = step.hashes[int(old_endpoint_index)]

        """Add attributes if they were not included directly"""
        # attributes -> null has been modified, remove if is confirmed
        """
        try:
            if  world.old_endpoint["attributes"] == "null":
                world.old_endpoint["attributes"] = None
        except:
            world.old_endpoint["attributes"] = None"""

        """Add defalt value of environment if not included"""

        try:
            if  world.old_endpoint["environment"] == "null":
                world.old_endpoint["environment"] = "production"
        except:
            world.old_endpoint["environment"] = "production"

        """The api_name has to be the one of the old capability"""
        api_name = world.old_capability[world.config["keys"]["api_name"]]
        world.old_endpoint[world.config["keys"]["api_name"]] = api_name

        """Send the request to check the endpoint using a URL template."""
        url_template = "$base_api_url/$apis_url/" + api_name + "/$endpoints_url/"
        rest_utils.request_the_resource(step, url_template)
        if requests.codes.ok == world.status_code and len(world.json) > 0:
            for received_endpoint in world.json:
                    """Delete previous endpoints"""
                    if self._check_endpoints_match(world.old_endpoint, received_endpoint):
                        rest_utils.delete_url(step, url_template + received_endpoint["id"])

        """Send the request to add the endpoint using the URL template."""
        rest_utils.send_to_url_the_data(step, url_template, world.old_endpoint)

        """Keep the id generated by the DB in world.old_endpoint.id too"""
        world.old_endpoint[world.config["keys"]["id"]] = \
            world.json[world.config["keys"]["id"]]

        """ Store de endpoint for future rule bindings """
        world.bindings.append(world.old_endpoint["id"])

    def an_instance_has_already_been_published_with_data(self, step, old_instance_index):
        """
        Publish through the API and keep in the world the instance data provided.
        :param step: Current Lettuce step.
        :param old_instance_index: Index of the instance data within the step.
        """

        """Generate attributes if they are provided in key value format"""
        try:
            world.old_instance = step.hashes[int(old_instance_index)]
            world.old_instance[world.config["keys"]["attributes"]] = rest_utils.generate_attributes(\
                step.hashes[int(old_instance_index)]["attributes_keys"], \
                step.hashes[int(old_instance_index)]["attributes_values"])

            del  world.old_instance["attributes_keys"]
            del  world.old_instance["attributes_values"]

        except:
            world.old_instance = step.hashes[int(old_instance_index)]

        """The classs_name has to be the one of the old class"""
        class_name = world.old_class[world.config["keys"]["class_name"]]
        world.old_instance[world.config["keys"]["class_name"]] = class_name

        """ If the class has previous instances that can collided with the currently published, \
        previous instances are deleted"""

        """Send the request to check the instance using a URL template."""
        url_template = "$base_api_url/$classes_url/" + class_name + "/$instances_url/"
        rest_utils.request_the_resource(step, url_template)

        if requests.codes.ok == world.status_code and len(world.json) > 0:
            for received_instance in world.json:
                    if self._check_instances_match(world.old_instance, received_instance):
                        rest_utils.delete_url(step, url_template + received_instance["id"])

        """Send the request to add the instance using the URL template."""
        rest_utils.send_to_url_the_data(step, url_template, world.old_instance)

        """Keep the id generated by the DB in world.old_instance.id too"""
        world.old_instance[world.config["keys"]["id"]] = \
            world.json[world.config["keys"]["id"]]

        """ Add environment=production if environment was not provided for instances assertion """
        try:

            if  world.old_instance["environment"] == "null":
                world.old_instance["environment"] = "production"
        except:
            world.old_instance["environment"] = "production"

        """ Store de instance for future rule bindings """
        world.bindings.append(world.old_instance["id"])

    def an_endpoint_has_not_already_been_published_with_data(self, step, old_endpoint_index):
        """
        Keep in the world the endpoint data provided without publishing it.
        :param step: Current Lettuce step.
        :param old_endpoint_index: Index of the endpoint data within the step.
        """
        world.old_endpoint = step.hashes[int(old_endpoint_index)]
        world.old_endpoint[world.config["keys"]["id"]] = \
            bson.ObjectId("5176a646255c2d27a87027d0")     # set an arbitrary id

    def an_instance_has_not_already_been_published_with_data(self, step, old_instance_index):
        """
        Keep in the world the instance data provided without publishing it.
        :param step: Current Lettuce step.
        :param old_instance_index: Index of the instance data within the step.
        """
        world.old_instance = step.hashes[int(old_instance_index)]
        world.old_instance[world.config["keys"]["id"]] = \
            bson.ObjectId("5176a646255c2d27a87027d0")     # set an arbitrary id

    def i_get_a_success_response_of_type_with_updated_capability_data(self, step, status_code):
        """
        Check that the response of the previous request has the type provided
        and the updated capability data, previously stored in the world.
        :param step: Current Lettuce step.
        :param status_code: Expected status code of the response.
        """
        rest_utils.get_a_success_response_of_type(step, status_code)
        self.the_response_contains_the_capability_data()

    def i_get_a_success_response_of_type_with_updated_class_data(self, step, status_code):
        """
        Check that the response of the previous request has the type provided
        and the updated capability data, previously stored in the world.
        :param step: Current Lettuce step.
        :param status_code: Expected status code of the response.
        """
        rest_utils.get_a_success_response_of_type(step, status_code)
        self.the_response_contains_the_class_data()

    def i_get_a_success_response_of_type_with_updated_endpoint_data(self, step, status_code):
        """
        Check that the response of the previous request has the type provided
        and the updated endpoint data, previously stored in the world.
        :param step: Current Lettuce step.
        :param status_code: Expected status code of the response.
        """
        rest_utils.get_a_success_response_of_type(step, status_code)
        self.the_response_contains_the_endpoint_data()

    def i_get_a_success_response_of_type_with_updated_instance_data(self, step, status_code):
        """
        Check that the response of the previous request has the type provided
        and the updated instance data, previously stored in the world.
        :param step: Current Lettuce step.
        :param status_code: Expected status code of the response.
        """
        rest_utils.get_a_success_response_of_type(step, status_code)
        self.the_response_contains_the_instance_data()

    def i_get_a_success_response_of_type_with_updated_binding_data(self, step, status_code):
        """
        Check that the response of the previous request has the type provided
        and the updated binding data, previously stored in the world.
        :param step: Current Lettuce step.
        :param status_code: Expected status code of the response.
        """
        rest_utils.get_a_success_response_of_type(step, status_code)
        self.the_response_contains_the_rule_data()

    def the_url_returns_the_capability_data(self, step, url):
        """
        Check that the URL provided points to a resource that contains the
        capability data previously stored in the world.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        """
        rest_utils.request_the_resource(step, url)
        rest_utils.get_a_success_response_of_type(step, requests.codes.ok)
        self.the_response_contains_the_capability_data()
        world.base_class = None

    def the_url_returns_the_class_data(self, step, url):
        """
        Check that the URL provided points to a resource that contains the
        capability data previously stored in the world.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        """
        rest_utils.request_the_resource(step, url)
        rest_utils.get_a_success_response_of_type(step, requests.codes.ok)
        self.the_response_contains_the_class_data()
        world.base_class = None

    def the_response_contains_the_capability_data(self):
        """
        Check that the response of the previous request contains the capability
        data previously stored in the world.
        """
        assert world.published_capability == world.json,\
        "Expected capability is not equivalent to returned capability. " \
                "Expected: %s. Received: %s." % (world.published_capability, world.json)

        """
        try:
            if (hasattr(world, "capability") and world.config["keys"]["description"] in world.capability) or \
                (hasattr(world, "old_capability") and world.config["keys"]["description"] in world.old_capability):
                description = world.json[world.config["keys"]["description"]]
            default_version = world.json[world.config["keys"]["default_version"]]
        except:
            assert False, "Error getting the capability data from the JSON: %s" \
            % world.json
        """

        """Check the description if it was previously set or it is being set now."""
        """
        if hasattr(world, "capability") and world.config["keys"]["description"] in world.capability:
            assert world.capability[world.config["keys"]["description"]] == description, \
                "Unexpected description received. Expected: %s. Received: %s." \
                % (world.capability[world.config["keys"]["description"]], description)
        elif hasattr(world, "old_capability") and world.config["keys"]["description"] in world.old_capability:
            assert world.old_capability[world.config["keys"]["description"]] == description, \
                "Unexpected description received. Expected: %s. Received: %s." \
                % (world.old_capability[world.config["keys"]["description"]], description)
        """
        """Check the default_version against its original value or the new one."""
        """
        if hasattr(world, "capability") and world.config["keys"]["default_version"] in world.capability:
            assert world.capability[world.config["keys"]["default_version"]] == default_version, \
                "Unexpected default_version received. Expected: %s. Received: %s." \
                % (world.capability[world.config["keys"]["default_version"]], default_version)
        else:
            assert world.old_capability[world.config["keys"]["default_version"]] == default_version, \
                "Unexpected default_version received. Expected: %s. Received: %s." \
                % (world.old_capability[world.config["keys"]["default_version"]], default_version)
        """

    def the_response_contains_the_class_data(self):
        """
        Check that the response of the previous request contains the class
        data previously stored in the world.
        """

        assert len(world.published_class) == len(world.json),\
        "Expected capability is not equivalent to returned capability. " \
                "Expected: %s. Received: %s." % (world.published_class, world.json)

        """ Check all the class parameters returned"""

        for key in world.published_class.keys():
            try:
                assert world.published_class[key] == world.json[key],\
                "Expected capability is not equivalent to returned capability. " \
                "Expected a %s: %s. Received: %s." % (key, world.published_class[key], world.json[key])
            except:
                assert False,\
                "Missing parameter in Json %s. " % key

    def the_url_returns_the_endpoint_data(self, step, url):
        """
        Check that the URL provided points to a resource that contains the
        endpoint data previously stored in the world.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        """
        rest_utils.request_the_resource(step, url)
        rest_utils.get_a_success_response_of_type(step, requests.codes.ok)
        self.the_response_contains_the_endpoint_data()

    def the_url_returns_the_instance_data(self, step, url):
        """
        Check that the URL provided points to a resource that contains the
        endpoint data previously stored in the world.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        """
        rest_utils.request_the_resource(step, url)
        rest_utils.get_a_success_response_of_type(step, requests.codes.ok)
        self.the_response_contains_the_instance_data()

    def the_url_returns_the_class_collection(self, step, url):
        """
        Check that the URL provided points to a resource that contains list of classes
        exposed in Service Directory
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        """
        rest_utils.request_the_resource(step, url)
        rest_utils.get_a_success_response_of_type(step, requests.codes.ok)
        self.the_response_contains_a_class_collection()

    def the_class_collection_contains_the_class(self, step, class_name):
        """
        Check that the class provided is inside the service class collection,
        requested previously
        :param step: Current Lettuce step.
        :param class_name: Class name to be validated
        """
        for class_item in world.json:
            if class_item[world.config["keys"]["class_name"]] == class_name:
                assert True, "The class %s is inside the class collection" % class_name
                return

        assert False, "The class  %s is not inside the class collection" % class_name

    def the_class_collection_not_contains_the_class(self, step, class_name):
        """
        Check that the class provided is not inside the service class collection,
        requested previously
        :param step: Current Lettuce step.
        :param class_name: Class name to be validated
        """
        for class_item in world.json:
            if class_item[world.config["keys"]["class_name"]] == class_name:
                assert False, "The class %s is inside the class collection" % class_name
                return

        assert True, "The class  %s is not inside the class collection" % class_name

    def the_response_contains_the_endpoint_data(self):
        """
        Check that the response of the previous request stored in world.json contains the endpoint data
        previously stored in the world.
        """

        try:
            api_name = world.json[world.config["keys"]["api_name"]]
            version = world.json[world.config["keys"]["version"]]
            url = world.json[world.config["keys"]["url"]]
            environment = world.json[world.config["keys"]["environment"]]
        except:
            assert False, "Error getting the endpoint data from the JSON: %s" \
            % world.json
        assert world.old_capability[world.config["keys"]["api_name"]] == api_name, \
            "Unexpected api_name received. Expected: %s. Received: %s." \
            % (world.old_capability[world.config["keys"]["api_name"]], api_name)
        assert world.endpoint[world.config["keys"]["version"]] == version, \
            "Unexpected version received. Expected: %s. Received: %s." \
            % (world.endpoint[world.config["keys"]["version"]], version)
        assert world.endpoint[world.config["keys"]["url"]] == url, \
            "Unexpected url received. Expected: %s. Received: %s." \
            % (world.endpoint[world.config["keys"]["url"]], url)

        """ Check if the endpoint was published with attributes and validate them """
        try:
            if world.config["keys"]["attributes"] in world.endpoint:
                expected_attributes = world.endpoint[world.config["keys"]["attributes"]]
                assert expected_attributes == world.json[world.config["keys"]["attributes"]], \
                "Unexpected attributes received. Expected: %s. Received: %s." \
                % (expected_attributes, world.json[world.config["keys"]["attributes"]])
        except:
                assert False, \
                "Missing attributes in the response. Received: %s." \
                % (world.json)

        """Get the expected environment value (production by default)"""
        if world.config["keys"]["environment"] in world.endpoint:
            expected_environment = world.endpoint[world.config["keys"]["environment"]]
        else:
            expected_environment = world.config["api_prefs"]["environment"]["default_value"]
        assert expected_environment == environment, \
            "Unexpected environment received. Expected: %s. Received: %s." \
            % (expected_environment, environment)

    def the_response_contains_the_instance_data(self):
        """
        Check that the response of the previous request stored in world.json contains the instance data
        previously stored in the world.
        """
        #TB refactor a reduce the coupling with Json values
        try:
            class_name = world.json[world.config["keys"]["class_name"]]
            version = world.json[world.config["keys"]["version"]]
            uri = world.json[world.config["keys"]["uri"]]
            environment = world.json[world.config["keys"]["environment"]]
        except:
            assert False, "Error getting the instance data from the JSON: %s" \
            % world.json
        assert world.old_class[world.config["keys"]["class_name"]] == class_name, \
            "Unexpected class_name received. Expected: %s. Received: %s." \
            % (world.old_class[world.config["keys"]["class_name"]], class_name)
        assert world.instance[world.config["keys"]["version"]] == version, \
            "Unexpected version received. Expected: %s. Received: %s." \
            % (world.instance[world.config["keys"]["version"]], version)
        assert world.instance[world.config["keys"]["uri"]] == uri, \
            "Unexpected url received. Expected: %s. Received: %s." \
            % (world.instance[world.config["keys"]["uri"]], uri)

        """ Check if the instance was published with attributes and validate them """
        try:
            if world.config["keys"]["attributes"] in world.instance:
                expected_attributes = world.instance[world.config["keys"]["attributes"]]
                assert expected_attributes == world.json[world.config["keys"]["attributes"]], \
                "Unexpected attributes received. Expected: %s. Received: %s." \
                % (expected_attributes, world.json[world.config["keys"]["attributes"]])
        except:
                assert False, \
                "Missing attributes in the response. Received: %s." \
                % (world.json)

        """Get the expected environment value (production by default)"""
        if world.config["keys"]["environment"] in world.instance:
            expected_environment = world.instance[world.config["keys"]["environment"]]
        else:
            expected_environment = world.config["api_prefs"]["environment"]["default_value"]
        assert expected_environment == environment, \
            "Unexpected environment received. Expected: %s. Received: %s." \
            % (expected_environment, environment)

    def the_response_contains_a_class_collection(self):
        """
        Check that the response of the previous request stored in world.json contains a class collection
        """

        for class_item in world.json:
            try:
                for key in class_item.keys():
                    assert key in world.config["keys"].keys(), \
                    "Expected class is not equivalent to returned class." \
                    "Key not reconigzed: %s" % key
            except:
                assert False,\
                        "Wrong class format: %s " % class_item

    def the_url_returns_an_error_of_type_with_error_code(self, step, url, status_code, code):
        """
        Check that when the resource of the URL provided is requested, the response
        has the type provided and a content consisting in a JSON element with the
        error code provided.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        :param status_code: Expected status code of the response.
        :param code: Expected error code in the JSON element.
        """
        rest_utils.request_the_resource(step, url)
        rest_utils.get_an_error_response_of_type_with_error_code(step, status_code, code)

    def the_resultset_contains_binding_in_position(self, step, binding_index, position=None):
        """
        Check that the resultset received in the response of the previous request
        contains a certain binding in the specified position.
        :param step: Current Lettuce step.
        :param binding_index: Index of the binding information within the step.
        :param position: Position where the binding should appear (optional).
        """

        expected_binding = self.generate_binding(step.hashes[int(binding_index)])

        """ Add stored data in the history for comparisson """

        expected_binding[world.config["keys"]["binding_rules"]] = [world.bindings_history.pop(0)]

        """ Restet the expected world binding once the expected binding is created and is not needed anymore"""
        world.binding = []
        world.binding_rules = []

        """Check if the binding is in the result set as expected"""
        if position == None:
            """Loop over the result set to find an binding that matches"""
            try:
                for received_binding in world.json:
                    if self._check_binding_match(expected_binding, received_binding):
                        return
            except:
                assert False, \
                    "Error getting bindings from the JSON: %s" % world.json
            assert False, \
                "Expected binding not contained in the JSON. " \
                "Expected: %s. JSON: %s." % (expected_binding, world.json)
        else:
            """Check that the binding received in the specified position matches"""
            pos = int(position)
            try:
                received_binding = world.json[pos]
            except:
                assert False, \
                    "Error getting the binding in position %d from the JSON: %s" \
                    % (pos, world.json)
            assert self._check_binding_match(expected_binding, received_binding), \
                "Expected binding not contained in position %d of the JSON. " \
                "Expected: %s. Received: %s." % (pos, expected_binding, received_binding)

    def the_resultset_contains_endpoint_in_position(self, step, endpoint_index, position=None):
        """
        Check that the resultset received in the response of the previous request
        contains a certain endpoint in the specified position.
        :param step: Current Lettuce step.
        :param endpoint_index: Index of the endpoint information within the step.
        :param position: Position where the endpoint should appear (optional).
        """

        """Generate attributes if they are provided in key value format"""

        expected_endpoint = self.generate_endpoint(step.hashes[int(endpoint_index)])

        """Add defalt value of environment if not included"""

        try:
            if  expected_endpoint["environment"] == "null":
                expected_endpoint["environment"] = "production"
        except:
            expected_endpoint["environment"] = "production"

        """ Recover instances to be validated """

        try:
            received_response = world.json
        except:
            assert False, \
                "Error getting endpoints from the JSON: %s" % world.json

        """Check if we have a list of instances or just one object"""

        if not isinstance(world.json, list):
            """Check if the endpoint is in the result set as expected"""
            assert self._check_endpoints_match(expected_endpoint, received_response), \
            "Expected endpoint not contained in JSON. " \
            "Expected: %s. Received: %s." % (expected_endpoint, received_response)
        else:
            if position is None:
                """Loop over the result set to find an endpoint that matches"""
                try:
                    for received_endpoint in received_response:
                        if self._check_endpoints_match(expected_endpoint, received_endpoint):
                            return
                except:
                    assert False, \
                        "Error getting endpoints from the JSON: %s" % received_response
                assert False, \
                    "Expected endpoint not contained in the JSON. " \
                    "Expected: %s. JSON: %s." % (expected_endpoint, received_response)
            else:
                """Check that the endpoint received in the specified position matches"""
                pos = int(position)
                try:
                    received_endpoint = received_response[pos]
                except:
                    assert False, \
                        "Error getting the endpoint in position %d from the JSON: %s" \
                        % (pos, received_response)
                assert self._check_endpoints_match(expected_endpoint, received_endpoint), \
                    "Expected endpoint not contained in position %d of the JSON. " \
                    "Expected: %s. Received: %s." % (pos, expected_endpoint, received_endpoint)

    def the_resultset_contains_instance_in_position(self, step, instance_index, position=None):
        """
        Check that the resultset received in the response of the previous request
        contains a certain endpoint in the specified position.
        :param step: Current Lettuce step.
        :param instance_index: Index of the endpoint information within the step.
        :param position: Position where the endpoint should appear (optional).
        """

        """Generate attributes if they are provided in key value format"""

        expected_instance = self.generate_instance(step.hashes[int(instance_index)])

        """Add defalt value of environment if not included"""

        try:
            if  expected_instance["environment"] == "null":
                expected_instance["environment"] = "production"
        except:
            expected_instance["environment"] = "production"

        """ Recover instances to be validated """

        try:
            received_response = world.json
        except:
            assert False, \
                "Error getting endpoints from the JSON: %s" % world.json

        """Check if we have a list of instances or just one object"""

        if not isinstance(world.json, list):
            """Check if the endpoint is in the result set as expected"""
            assert self._check_instances_match(expected_instance, received_response), \
            "Expected instance not contained in JSON. " \
            "Expected: %s. Received: %s." % (expected_instance, received_response)
        else:
            if position == None:
                """Loop over the result set to find an endpoint that matches"""
                try:
                    for received_instance in received_response:
                        if self._check_instances_match(expected_instance, received_instance):
                            return
                except:
                    assert False, \
                        "Error getting instances from the JSON: %s" % received_response
                assert False, \
                    "Expected instance not contained in the JSON. " \
                    "Expected: %s. JSON: %s." % (expected_instance, received_response)
            else:
                """Check that the instance received in the specified position matches"""
                pos = int(position)
                try:
                    received_instance = received_response[pos]
                except:
                    assert False, \
                        "Error getting the instance in position %d from the JSON: %s" \
                        % (pos, received_response)
                assert self._check_instances_match(expected_instance, received_instance), \
                    "Expected instance not contained in position %d of the JSON. " \
                    "Expected: %s. Received: %s." % (pos, expected_instance, received_instance)

    def _check_binding_match(self, expected_binding, received_binding):
        """
        Check that the endpoint provided matches another endpoint, also provided,
        that was received in a query. The id field of the latter is ignored.
        :param expected_binding: Binding expected to be received.
        :param received_binding: Binding received in the query.
        """
        if len(expected_binding) != len(received_binding) - 1:
            return False
        try:
            for key in expected_binding:
                if not key in received_binding:
                    return False
                elif expected_binding[key] != received_binding[key]:
                    return False
        except:
            return False

        return True

    def _check_endpoints_match(self, expected_endpoint, received_endpoint):
        """
        Check that the endpoint provided matches another endpoint, also provided,
        that was received in a query. The id field of the latter is ignored.
        :param expected_endpoint: Endpoint expected to be received.
        :param received_endpoint: Endpoint received in the query.
        """
        if len(expected_endpoint) != len(received_endpoint) - 1:
            return False

        try:
            for key in expected_endpoint:
                if not key in received_endpoint:
                    return False
                elif expected_endpoint[key] != received_endpoint[key]:
                    return False
        except:
            return False

        return True

    def _check_instances_match(self, expected_instance, received_instance):
        """
        Check that the endpoint provided matches another instance, also provided,
        that was received in a query. The id field of the latter is ignored.
        Comparing only uri and version.
        :param expected_instance: Instance expected to be received.
        :param received_instance: Instance received in the query.
        """

        try:
            if expected_instance[world.config["keys"]["uri"]] != received_instance[world.config["keys"]["uri"]]:
                return False
            if expected_instance[world.config["keys"]["version"]] != \
            received_instance[world.config["keys"]["version"]]:
                return False
        except:
            return False

        return True

    def the_response_contains_the_rule_data(self):
        """
        Check that the response of the previous request contains the rule data
        previously stored in the world.
        """

        """Check if the binding contais the id"""

        binding_id = world.json.pop(world.config["keys"]["binding_id"])
        #TDB include the Mongo object _id length
        binding_validator = re.compile("^[a-z0-9]{1,50}$")

        try:
            assert binding_id in binding_validator.match(binding_id).group(),\
            "Expected binding format is not equivalent to returned format. " \
            "Expected: %s. Received: %s." % (world.published_rules, world.json)
        except:
            assert False,\
            "Expected binding format is not equivalent to returned format. " \
            "Expected: %s. Received: %s." % (world.published_rules, world.json)

        assert world.published_rules == world.json,\
        "Expected context rules are not equivalent to returned rules. " \
                "Expected: %s. Received: %s." % (world.published_rules, world.json)

    def the_url_returns_the_rule_data(self, step, url):
        """
        Check that the URL provided points to a resource that contains the
        rule data previously stored in the world.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        """
        rest_utils.request_the_resource(step, url)
        rest_utils.get_a_success_response_of_type(step, requests.codes.ok)
        self.the_response_contains_the_rule_data()

    def process_rules_values(self, rule):
        """
        Process the values provided in lettuce to generate a valid rules values strucutre.
        :param rule: Current rule in the step.
        """
        temp_values = []
        for item in rule["value"].split(","):
            temp_values.append(rest_utils.prepare_plain_data(item))
        return temp_values

    def the_following_bindings_rules_are_avalilabe(self, step, operation_index):
        """
        Creates the rules structure for a context to be published.
        :param step: Current Lettuce step.
        :param operation_index: Index of the rule operation within the step.
        """

        try:
            # keyword [all] in lettuce table joins tables entries in one list
            if  "all" in operation_index:
                for item in step.hashes:
                    item["value"] = self.process_rules_values(item)
                    world.rules = step.hashes
            else:
                world.rules = step.hashes[int(operation_index)]
                world.rules["value"] = self.process_rules_values(step.hashes[int(operation_index)])
                world.rules = [rest_utils.prepare_plain_data(world.rules)]

            # Modification of JSON to generate a JSON no valid log trace
            for items in world.rules:
                try:
                    if "[BAD_JSON]" in  items["value"]:
                            items["value"] = [{"bad_json": "bad_json"}]
                except:
                    continue

        except:
            world.rules = []

        world.binding_rules.append({world.config["keys"]["group_rules"]: world.rules, \
                                     "bindings": copy.copy(world.bindings)})

        """ Reset Bindings for next rules group and increment endpoints historical resgistry"""
        world.endpoints_history.extend(world.bindings)
        world.instances_history.extend(world.bindings)
        world.bindings_history.extend(copy.copy(world.binding_rules))
        world.bindings = []

    def the_following_bindings_are_available_for_the_context_rules(self, step, binding_index):

        if "[EMPTY_BINDINGS]" in step.hashes[int(binding_index)]["bindings"]:
            world.bindings = []
        else:
            world.bindings = [step.hashes[int(binding_index)]["bindings"]]

    def the_exceptiontext_contains_exceptiontext(self, step, exceptionText_index):
        expected_message = step.hashes[int(exceptionText_index)]["exceptionText"]
        rest_utils.get_an_error_response_message(step, expected_message)

    def get_endpoint_id(self, position):
        return world.endpoints_history[int(position)]

    def get_instance_id(self, position):
        return world.instances_history[int(position)]

    def the_url_returns_the_user_data(self, step, url):
        """
        Check that the URL provided points to a resource that contains the
        user data previously stored in the world.
        :param step: Current Lettuce step.
        :param url: Template of the URL where to send the request.
        """
        rest_utils.request_the_resource(step, url)
        rest_utils.get_a_success_response_of_type(step, requests.codes.ok)
        self.the_response_contains_the_user_data()

    def the_response_contains_the_user_data(self):

        """
        Check that the response of the previous request contains the user data
        previously stored in the world. Add parameters that are automatically added by
        the SD if they are not provided.
        """

        """Add default value for is_admin"""
        try:
            world.created_user["is_admin"]
        except:
            world.created_user["is_admin"] = False

        """Add default value for classes"""
        try:
            world.created_user["classes"]
        except:
            world.created_user["classes"] = []

        """Add default value for origins"""
        try:
            world.created_user["origins"]
        except:
            world.created_user["origins"] = []

        """Hide the password"""
        world.created_user["password"] = "****"

        assert world.created_user == world.json,\
        "Expected user is not equivalent to returned user. " \
                "Expected: %s. Received: %s." % (world.created_user, world.json)

    def reset_SD(self):

        # "SD API: Remote clean-up"
        url_classes_template = "$base_api_url/$classes_url/"
        url_bindings_template = "$base_api_url/$bindings_url/"
        url_users_template = "$base_api_url/$users_url/"

        """Get the URL with values from the template."""
        url_classes = rest_utils._get_url_with_values(url_classes_template)
        url_bindings = rest_utils._get_url_with_values(url_bindings_template)
        url_users = rest_utils._get_url_with_values(url_users_template)

        """ Set the user for the deletion process """
        auth = ("admin", "admin")

        """Send the request to obtain the published data in the SD"""
        try:
            res_classes = requests.get(url_classes, auth=auth)
            res_bindings = requests.get(url_bindings, auth=auth)
            res_users = requests.get(url_users, auth=auth)
        except:
            assert False, "Django server connection error."

        """Proccess the request to obtain all the bindings ID and delete them"""
        try:
            bindings_json = res_bindings.json()
            for binding in bindings_json:
                print 'Delete binding: ', str(binding)
                requests.delete(url_bindings + binding[world.config["keys"]["id"]], auth=auth)
        except:
            bindings_json = None

        """Proccess the request to obtain all the classes and the instances and delete them"""
        try:
            classes_json = res_classes.json()
            for class_obj in classes_json:
                print 'Delete class: ', str(class_obj)
                instances_json = (requests.get(url_classes + class_obj["class_name"] + "/instances", auth=auth)).json()
                for instance in instances_json:
                    print 'Delete instance: ', instance
                    requests.delete(url_classes + class_obj["class_name"] + "/instances/" + instance["id"], auth=auth)
                requests.delete(url_classes + class_obj["class_name"], auth=auth)
        except:
            classes_json = None

        """Proccess the request to obtain all the users and delete all of them except admin user"""
        try:
            users_json = res_users.json()
            for user in users_json:
                print 'Delete user: ', str(user)
                if user["username"] not in "admin":
                    requests.delete(url_bindings + user["username"], auth=auth)
        except:
            users_json = None

    def validate_correlator(self, expected_correlator):
        assert(re.search(expected_correlator, world.correlator)), \
        "Expected correlator is not equivalent to returned correlator. " \
                "Expected: %s. Received: %s." % (expected_correlator, world.correlator)
