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
from commons.views import CustomGenericAPIView, check_duplicated_query_params,\
    check_empty_query_params, check_regex_query_params
from rest_framework.response import Response
from classes.services import ServiceClassService, ServiceInstanceService
from classes.serializers import ServiceClassCollectionSerializer, ServiceInstanceSerializer,\
    ServiceClassItemSerializer, ServiceInstanceItemSerializer
from commons.serializers import serialize_to_response, deserialize_input
from django.conf import settings
from users.authentication import IsAdminOrClassPermissionOrReadOnly, IsAdminOrReadOnly


class ServiceClassCollectionView(CustomGenericAPIView):
    serializer_class = ServiceClassCollectionSerializer
    service_class = ServiceClassService

    permission_classes = (IsAdminOrReadOnly, )

    @serialize_to_response(many=True)
    def get(self, request, *args, **kwargs):
        return self.service.get_all_service_classes()

    @serialize_to_response(many=False, status_code=status.HTTP_201_CREATED)
    @deserialize_input(partial=False)
    def post(self, request, *args, **kwargs):
        # kwargs['deserialized_object'] has been deseralized and validated
        return self.service.create(kwargs['deserialized_object'])


class ServiceClassItemView(CustomGenericAPIView):
    serializer_class = ServiceClassItemSerializer
    service_class = ServiceClassService

    permission_classes = (IsAdminOrClassPermissionOrReadOnly, )

    @serialize_to_response(many=False)
    def get(self, request, *args, **kwargs):
        return self.service.get(kwargs['class_name'])

    @serialize_to_response(many=False, status_code=status.HTTP_200_OK)
    @deserialize_input(partial=True)
    def post(self, request, *args, **kwargs):
        return self.service.update(kwargs['deserialized_object'])

    @serialize_to_response(status_code=status.HTTP_204_NO_CONTENT)
    def delete(self, request, *args, **kwargs):
        return self.service.delete(kwargs['class_name'])


class ServiceInstanceView(CustomGenericAPIView):
    """
    View for dealing with collection instances
    """
    serializer_class = ServiceInstanceSerializer
    service_class = ServiceInstanceService

    permission_classes = (IsAdminOrClassPermissionOrReadOnly, )

    @serialize_to_response(many=True, status_code=status.HTTP_200_OK)
    @check_regex_query_params(settings.QUERY_PARAMS_GET_ENDPOINTS)
    @check_duplicated_query_params
    @check_empty_query_params
    def get(self, request, *args, **kwargs):

        # Transforms the dictionary key to lowerCase and exclude filters query param
        filter_param = settings.REQUEST_FILTER_PARAM
        request_params = dict(((key.lower(), value) for key, value in request.QUERY_PARAMS.items()
                                                        if key not in (filter_param,)))

        return self.service.discover_service_instances(kwargs['class_name'], request_params)

    @serialize_to_response(many=False, status_code=status.HTTP_201_CREATED)
    @deserialize_input(partial=False)
    def post(self, request, *args, **kwargs):
        # kwargs['deserialized_object'] has been deseralized and validated
        return self.service.create(kwargs['deserialized_object'])


class ServiceInstanceItemView(CustomGenericAPIView):
    """
    View for modifying a single instance
    """

    serializer_class = ServiceInstanceSerializer
    serializer_class_put = ServiceInstanceItemSerializer
    service_class = ServiceInstanceService

    permission_classes = (IsAdminOrClassPermissionOrReadOnly, )

    @serialize_to_response(many=False, status_code=status.HTTP_200_OK)
    def get(self, request, *args, **kwargs):
        return self.service.get_service_instance(kwargs['class_name'], kwargs['id'])

    @serialize_to_response(many=False, status_code=status.HTTP_200_OK)
    @deserialize_input(partial=False)
    def put(self, request, *args, **kwargs):
        return self.service.update(kwargs['deserialized_object'])

    @serialize_to_response(status_code=status.HTTP_204_NO_CONTENT)
    def delete(self, request, *args, **kwargs):
        return self.service.delete(kwargs['class_name'], kwargs['id'])


class InfoView(CustomGenericAPIView):

    def get(self, request, *args, **kwargs):
        return Response({'app_name': settings.APP_NAME, 'default_version': settings.VERSION},
                    status=status.HTTP_200_OK)
