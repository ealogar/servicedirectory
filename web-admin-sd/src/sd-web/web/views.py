"""
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
"""

import logging
from django.shortcuts import render_to_response
from django.views.generic import TemplateView, FormView
from web.forms import CapForm, RemoveCapForm, EndpointForm, ModifyEndpointForm, RemoveEndpoint
from web.services import CapabilitiesService, EndpointsService

logger = logging.getLogger(__name__)


class HomeTemplateView(TemplateView):
    template_name = 'empty_template.html'

    def get_context_data(self, **kwargs):
        return {'title': 'Service Directory - Home'}


class SearchCapTemplateView(TemplateView):
    template_name = 'empty_template.html'

    def get_context_data(self, **kwargs):
        return {'title': 'Service Directory - Search Capability'}


class SearchEndTemplateView(TemplateView):
    template_name = 'empty_template.html'

    def get_context_data(self, **kwargs):
        return {'title': 'Service Directory - Search Endpoint'}


class AddCapTemplateView(TemplateView):
    template_name = 'addCap.html'

    def get_context_data(self, **kwargs):
        return {'title': 'Service Directory - Add Capability'}


class AddCapFormView(FormView):
    template_name = 'addCap.html'
    form_class = CapForm
    service = CapabilitiesService()

    def form_valid(self, form):
        logger.debug(' '.join(['Adding capability', form.cleaned_data['api_name']]))
        result = self.service.create_capability(form.cleaned_data)
        if 'body' in result:
            result['title'] = 'Creation Failure'
        else:
            result['title'] = 'Capability created'
        return render_to_response('form_result.html', result)


class CapabilitiesRemoveFormView(FormView):
    form_class = RemoveCapForm

    service = CapabilitiesService()

    def form_valid(self, form):
        logger.debug(' '.join(['Removing capability', form.cleaned_data['api_name']]))
        result = self.service.remove_capability(form.cleaned_data['api_name'])
        if 'body' in result:
            result['title'] = 'Deletion Failure'
        else:
            result['title'] = 'Capability Removed'
        return render_to_response('form_result.html', result)


class CapabilityModificationFormView(FormView):
    form_class = CapForm
    service = CapabilitiesService()

    def form_valid(self, form):
        logger.debug(' '.join(['Updating capability', form.cleaned_data['api_name']]))
        result = self.service.modify_capability(form.cleaned_data)
        if 'body' in result:
            result['title'] = 'Updated Failure'
        else:
            result['title'] = 'Capability Updated'
        return render_to_response('form_result.html', result)


class CapabilitiesTemplateView(TemplateView):
    template_name = 'capabilities.html'
    service = CapabilitiesService()

    def get_context_data(self, **kwargs):
        capabilities = self.service.get_capabilities()
        for capability in capabilities:
            capability['web_href'] = ''.join([capability['api_name'], '/endpoints'])

        return {'title': 'Service Directory - Capabilities', 'capabilities': capabilities}


class EndpointsTemplateView(TemplateView):
    template_name = 'endpoints.html'
    service = EndpointsService()

    def get_context_data(self, **kwargs):

        endpoints = self.service.get_endpoints(kwargs['api_name'])

        return {'title': 'Service Directory - Endpoints', 'api_name': kwargs['api_name'],
                'endpoints': endpoints}


class AddEndpointFormView(FormView):
    form_class = EndpointForm
    service = EndpointsService()

    def form_valid(self, form):
        logger.debug(' '.join(['Adding endpoint to capability', form.cleaned_data['api_name']]))
        result = self.service.addEndpoint(form.cleaned_data)
        if 'body' in result:
            result['title'] = 'Creation Failure'
        else:
            result['title'] = 'EndPoint Added'
        return render_to_response('form_result.html', result)


class EditEndpointFormView(FormView):
    form_class = ModifyEndpointForm
    service = EndpointsService()

    def form_valid(self, form):
        logger.debug(' '.join(['Adding endpoint to capability', form.cleaned_data['api_name']]))
        result = self.service.modifyEndpoint(form.cleaned_data)
        if 'body' in result:
            result['title'] = 'Update Failure'
        else:
            result['title'] = 'EndPoint updated'
        return render_to_response('form_result.html', result)


class RemoveEndpointFormView(FormView):
    form_class = RemoveEndpoint
    service = EndpointsService()

    def form_valid(self, form):
        logger.debug(' '.join(['Removing endpoint ', form.cleaned_data['id_end'], ' of capability',
                               form.cleaned_data['api_name']]))
        result = self.service.removeEndpoint(form.cleaned_data)
        if 'body' in result:
            result['title'] = 'Remove Failure'
        else:
            result['title'] = 'EndPoint Removed'
        return render_to_response('form_result.html', result)


