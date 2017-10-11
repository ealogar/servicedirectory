'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from django.conf.urls.defaults import patterns, include, url
from bindings.views import BindingInstanceView, BindingsCollectionView, BindingsItemView
from classes.views import InfoView
from django.conf import settings
from commons.views import handle_default_404, handle_default_500

urlpatterns = patterns('',

    url(r'^sd/{version}/classes'.format(version=settings.VERSION), include('classes.urls'), {'SSL': True}),
    url(r'^sd/{version}/users'.format(version=settings.VERSION), include('users.urls'), {'SSL': True}),

    url(r'^sd/{version}/bindings/?$'.format(version=settings.VERSION),
        BindingsCollectionView.as_view(), {'SSL': True}, name='bindings_collection'),
    url(r'^sd/{version}/bindings/(?P<id>[\w]+)/?$'.format(version=settings.VERSION),
        BindingsItemView.as_view(), {'SSL': True}, name='bindings_detail'),
    url(r'^sd/{version}/bind_instances/?$'.format(version=settings.VERSION),
        BindingInstanceView.as_view(), name='bind_instance'),

    url(r'^sd/info/?', InfoView.as_view())
)

# Define default 404 and 500 errors for django
handler404 = handle_default_404
handler500 = handle_default_500
