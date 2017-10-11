'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''

from django import forms


class CapForm(forms.Form):
    api_name = forms.CharField(required=True)
    description = forms.CharField(required=False)
    default_version = forms.CharField(required=True)


class RemoveCapForm(forms.Form):
    api_name = forms.CharField(required=True)


class EndpointForm(forms.Form):
    api_name = forms.CharField(required=True)
    environment = forms.CharField(required=True)
    version = forms.CharField(required=True)
    url = forms.CharField(required=True)
    ob = forms.CharField(required=False)
    premium = forms.BooleanField(required=False)


class ModifyEndpointForm(forms.Form):
    api_name = forms.CharField(required=True)
    environment = forms.CharField(required=True)
    version = forms.CharField(required=True)
    url = forms.CharField(required=True)
    ob = forms.CharField(required=False)
    premium = forms.BooleanField(required=False)
    id_end = forms.CharField(required=True)


class RemoveEndpoint(forms.Form):
    api_name = forms.CharField(required=True)
    id_end = forms.CharField(required=True)
