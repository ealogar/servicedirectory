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
from users.views import UsersCollectionView, UsersItemView
from django.conf import settings


urlpatterns = patterns('',
    url(r'^/?$', UsersCollectionView.as_view(), name='users_col'),
    url(r'^/(?P<username>{0})/?$'.format(settings.USER_NAME_REGEX), UsersItemView.as_view(), name='user_detail')
)
