"""
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
"""

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.conf import settings

from web.auth_views import LoginView
from web.views import HomeTemplateView, SearchCapTemplateView, SearchEndTemplateView, \
    CapabilitiesTemplateView, EndpointsTemplateView, AddCapFormView, CapabilitiesRemoveFormView,\
    CapabilityModificationFormView, AddEndpointFormView, EditEndpointFormView, RemoveEndpointFormView
from web.auth_views import LogoutView


urlpatterns = patterns('',
                       url(r'^(/?|/login/?)$', LoginView.as_view(), name='login'),
                       url(r'^/logout/?$', LogoutView.as_view(), name='logout'),
                       url(r'^/home/?$',
                           login_required(function=HomeTemplateView.as_view(),
                                          login_url=settings.LOGGING_URL),
                           name='home'),

                       url(r'^/searchCap/?$',
                           login_required(function=SearchCapTemplateView.as_view(),
                                          login_url=settings.LOGGING_URL), name='searchCap'),
                       url(r'^/searchEnd/?$',
                           login_required(function=SearchEndTemplateView.as_view(),
                                          login_url=settings.LOGGING_URL), name='searchEnd'),

                       # url(r'^(addCap/?)$', AddCapTemplateView.as_view(), name='addCap'),
                       url(r'^/addCap/?$',
                           login_required(function=AddCapFormView.as_view(),
                                          login_url=settings.LOGGING_URL), name='addCap'),

                       url(r'^/capabilities/?$',
                           login_required(function=CapabilitiesTemplateView.as_view(),
                                          login_url=settings.LOGGING_URL), name='capabilities'),


                       url(r'^/capabilities/endpoints/removeEnd/?$',
                           login_required(function=RemoveEndpointFormView.as_view(),
                                          login_url=settings.LOGGING_URL), name='remEndpoints'),


                       url(r'^/(?P<api_name>[a-zA-Z0-9_-]+)/(endpoints/?)',
                           login_required(function=EndpointsTemplateView.as_view(),
                                          login_url=settings.LOGGING_URL), name='endpoints'),


                       url(r'^/capabilities/remove/?$',
                           login_required(function=CapabilitiesRemoveFormView.as_view(),
                                          login_url=settings.LOGGING_URL), name='removeCapabilities'),

                       url(r'^/(capabilities/addEnd?)$',
                           login_required(function=AddEndpointFormView.as_view(),
                                          login_url=settings.LOGGING_URL), name='addEndpoint'),

                       url(r'^/(capabilities/editEnd?)$',
                           login_required(function=EditEndpointFormView.as_view(),
                                          login_url=settings.LOGGING_URL),
                           name='editEndpoint'),

                       url(r'^/(editCap/?)$',
                           login_required(function=CapabilityModificationFormView.as_view(),
                                          login_url=settings.LOGGING_URL), name='modifyCapSubmit'),

)
