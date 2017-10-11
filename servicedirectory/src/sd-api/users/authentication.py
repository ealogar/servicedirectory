'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from __future__ import unicode_literals  # Make all strings in file converted to unicode
from rest_framework.authentication import BasicAuthentication
from commons.singleton import Singleton
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, AnonymousUser
from django.conf import settings
import logging
from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.services import UserAdminService
from commons.exceptions import NotFoundException

logger = logging.getLogger(__name__)


class BasicMongoAuthentication(BasicAuthentication):
    """
    Overrides BasicAuthentication in rest framework to authenticate credentials
    with users collection in Mongo Database
    """
    __metaclass__ = Singleton  # avoid checking init every time a request is done

    def __init__(self):
        self.service = UserAdminService()
        # Ensure default admin user is created
        try:
            default_user = settings.SD_USERNAME
            default_password = settings.SD_PASSWORD
        except AttributeError:
            logger.error("Default admin credentials not found in config")
            return

        try:
            self.service.get_user(default_user)
        except NotFoundException:
            try:
                self.service.create({'_id': default_user, 'password': default_password,
                                              'is_admin': True})
            except Exception as e:
                logger.error('Default Admin user could not be created %s', str(e))

    def authenticate_credentials(self, userid, password):
        """
        Authenticate the userid and password against username and password.
        """
        try:
            user = self.service.get_user(userid)
            if user:
                # Check that encoded password in database matches with password given
                if check_password(password, user['password']):
                    # Transform user dict into django User model
                    django_user = User(username=user['_id'], password=user['password'],
                                       is_staff=user['is_admin'])
                    # add classes for custom permissions with mongo
                    django_user.classes = user.get('classes', ())
                    django_user.origins = user.get('origins', ())
                    return (django_user, None)
        except NotFoundException:
            pass
        except Exception as e:
            logger.error('Error in authenticate method %s', str(e))
            raise e

        raise AuthenticationFailed('Invalid username/password')


class IsAdminOrOriginPermissionOrReadOnly(BasePermission):
    """
    Gives permission when authenticated user has the property is_staff=true
    or has permission to access the client rules of the view:
         view['origin'] in user.classes collection
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user:
            if request.user.is_staff:
                return True
            elif isinstance(request.user, AnonymousUser):
                return False
            else:
                try:
                    # default client can be accessed by class
                    origin = request.DATA['origin']
                    if origin == 'default':
                        if request.DATA['class_name'] in request.user.classes:
                            return True
                    else:
                        # check if user has permissions over rules
                        if origin in request.user.origins:
                            return True
                except (AttributeError, KeyError):
                    # classes and origins not defined we will delegate the logic to
                    # has_object_permission
                    return True
        return False

    def has_object_permission(self, request, view, obj):

        if request.user:
            # Check if we have an admin user
            if request.user.is_staff:
                return True
            else:
                # Check origin permission
                if obj['origin'] == 'default':
                    if obj['class_name'] in request.user.classes:
                        return True
                else:
                    # check if user has permissions over rules
                    if obj['origin'] in request.user.origins:
                        return True
        return False


class IsAdminOrReadOnly(BasePermission):
    """
    Gives permission when authenticated user has the property is_staff=true
    or has permission to access the class of the view:
         view['class_name'] in user.classes collection
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (request.user and request.user.is_staff)


class IsAdminUserOrReadHimself(BasePermission):
    """
    Gives access to Admin user or read access when the authenticated
    users is same than the username in requests (not put or delete).
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or
        request.user.username == view.kwargs['username'])


class IsAdminOrClassPermissionOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        try:
            # Recover class_name from url and if not in DATA (priority of url)
            return request.user and (request.user.is_staff or view.kwargs['class_name'] in request.user.classes)
        except (AttributeError, KeyError):
            return False
