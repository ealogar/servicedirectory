'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from django.conf.urls.defaults import patterns, url
from classes.views import ServiceClassCollectionView, ServiceInstanceView, ServiceClassItemView,\
 ServiceInstanceItemView
from django.conf import settings

urlpatterns = patterns('',
    url(r'^/(?P<class_name>{class_})/instances/?$'.format(class_=settings.CLASS_NAME_REGEX),
        ServiceInstanceView.as_view()),
    url(r'^/(?P<class_name>{class_})/instances/(?P<id>[\w]+)/?$'.format(class_=settings.CLASS_NAME_REGEX),
        ServiceInstanceItemView.as_view(), name='instance_detail'),

    url(r'^/?$',
        ServiceClassCollectionView.as_view()),
    url(r'^/(?P<class_name>{class_})/?$'.format(class_=settings.CLASS_NAME_REGEX),
        ServiceClassItemView.as_view(), name='class_detail')
)
