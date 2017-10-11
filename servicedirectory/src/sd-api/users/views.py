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
from commons.views import CustomGenericAPIView
from commons.serializers import serialize_to_response, deserialize_input
from rest_framework.permissions import IsAdminUser
from users.serializers import UserCollectionSerializer, UserItemSerializer
from users.services import UserAdminService
from users.authentication import IsAdminUserOrReadHimself


class UsersCollectionView(CustomGenericAPIView):
    serializer_class = UserCollectionSerializer
    service_class = UserAdminService

    permission_classes = (IsAdminUser, )

    @serialize_to_response(many=True)
    def get(self, request, *args, **kwargs):
        return self.service.get_all_users()

    @serialize_to_response(many=False, status_code=status.HTTP_201_CREATED)
    @deserialize_input(partial=False)
    def post(self, request, *args, **kwargs):
        return self.service.create(kwargs['deserialized_object'])


class UsersItemView(CustomGenericAPIView):
    serializer_class = UserItemSerializer
    service_class = UserAdminService

    permission_classes = (IsAdminUserOrReadHimself, )

    @serialize_to_response(many=False)
    def get(self, request, *args, **kwargs):
        return self.service.get_user(kwargs['username'])

    @serialize_to_response(many=False, status_code=status.HTTP_200_OK)
    @deserialize_input(partial=True)
    def post(self, request, *args, **kwargs):
        return self.service.update(kwargs['deserialized_object'], request.user.username)

    @serialize_to_response(status_code=status.HTTP_204_NO_CONTENT)
    def delete(self, request, *args, **kwargs):
        return self.service.delete(kwargs['username'], request.user.username)
