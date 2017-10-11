'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from rest_framework import status
from django.conf import settings
from bindings.serializers import BindingsSerializer, BindingInstanceSerializer
from bindings.services import BindingService

from commons.views import CustomGenericAPIView, check_duplicated_query_params,\
    check_empty_query_params, check_regex_query_params
from classes.serializers import ServiceInstanceSerializer
from commons.serializers import serialize_to_response, deserialize_input
from users.authentication import IsAdminOrOriginPermissionOrReadOnly


class BindingInstanceView(CustomGenericAPIView):
    """
    View for dealing with bind instance (best instance for an origin)
    """
    serializer_class = ServiceInstanceSerializer
    service_class = BindingService

    @serialize_to_response(many=False, status_code=status.HTTP_200_OK)
    @check_regex_query_params(settings.INPUT_CONTEXT_KEYS_REGEX)
    @check_duplicated_query_params
    @check_empty_query_params
    def get(self, request, *args, **kwargs):

        request_params = self.lower_query_params(request, settings.REQUEST_FILTER_PARAM)
        return self.service.get_binding_instance(request_params)


class BindingsCollectionView(CustomGenericAPIView):
    serializer_class = BindingsSerializer
    service_class = BindingService

    permission_classes = (IsAdminOrOriginPermissionOrReadOnly, )

    @serialize_to_response(many=True)
    @check_regex_query_params(settings.QUERY_PARAMS_GET_BINDINGS)
    @check_duplicated_query_params
    @check_empty_query_params
    def get(self, request, *args, **kwargs):
        request_params = self.lower_query_params(request, settings.REQUEST_FILTER_PARAM)
        return self.service.get_all_bindings(request_params)

    @serialize_to_response(many=False, status_code=status.HTTP_201_CREATED)
    @deserialize_input(partial=False)
    def post(self, request, *args, **kwargs):
        return self.service.create_binding(kwargs['deserialized_object'])


class BindingsItemView(CustomGenericAPIView):
    serializer_class = BindingInstanceSerializer
    service_class = BindingService

    permission_classes = (IsAdminOrOriginPermissionOrReadOnly, )

    # We can not use default permission_classes here
    # we use object level security as the instance_id is not fully
    # related with authenticated user

    @serialize_to_response(many=False)
    def get(self, request, *args, **kwargs):
        return self.service.get_binding_by_id(kwargs['id'])

    @serialize_to_response(status_code=status.HTTP_204_NO_CONTENT)  # generate response
    def delete(self, request, *args, **kwargs):
        # Check object permission
        obj = self.service.get_binding_by_id(kwargs['id'])
        self.check_object_permissions(request, obj)

        return self.service.delete_binding(kwargs['id'])

    @serialize_to_response(many=False)
    @deserialize_input(partial=False)
    def put(self, request, *args, **kwargs):
        # check object permission
        obj = self.service.get_binding_by_id(kwargs['id'])
        self.check_object_permissions(request, obj)

        return self.service.update_binding(kwargs['deserialized_object'])
