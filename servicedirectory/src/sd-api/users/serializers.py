'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from commons.serializers import SchemaSerializer
from users.services import UserAdminService
from commons.exceptions import NotFoundException
from commons.fields import  MultipleSerializerField, PasswordField, RegexRestricField
import logging
from django.core.exceptions import ValidationError
from re import match
from django.conf import settings
from django.contrib.auth.hashers import make_password


logger = logging.getLogger(__name__)


class UserCollectionSerializer(SchemaSerializer):
    """
    Serializer class for user collection
    """
    username = RegexRestricField('^{0}$'.format(settings.USER_NAME_REGEX), min_length=1, max_length=512,
                                 source='_id', required=True)
    password = PasswordField(required=True, min_length=1, max_length=512)
    classes = MultipleSerializerField(required=False)
    origins = MultipleSerializerField(required=False)

    def validate_classes(self, attrs, source):

        for class_ in attrs.get(source, ()):
            if not match('^{0}$'.format(settings.CLASS_NAME_REGEX), class_):
                raise ValidationError(self.error_messages['invalid'])
        return attrs

    def validate_origins(self, attrs, source):

        for origin in attrs.get(source, ()):
            if not match(settings.ORIGIN_REGEX, origin):
                raise ValidationError(self.error_messages['invalid'])
        return attrs

    class Meta:
        schema = 'UserModel'
        view_item_name = 'user_detail'
        # _id instead of 'class_name' because the source of class_name is _id
        url_fields = ('_id',)
        # _id field of schema will be mapped in user_name
        exclude = ('_id',)


class UserItemSerializer(UserCollectionSerializer):

    def restore_object(self, attrs, instance=None):
        try:
            instance = UserAdminService().get_user(self.context['username'])
        except NotFoundException as e:
            raise e

        # If password has to be updated, make hash to store in database
        if 'password' in attrs:
            attrs['password'] = make_password(attrs['password'])
        return super(UserItemSerializer, self).restore_object(attrs, instance=instance)
