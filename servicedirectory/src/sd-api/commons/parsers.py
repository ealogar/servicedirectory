'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
from rest_framework.parsers import BaseParser
from django.conf import settings
import json
from rest_framework.exceptions import ParseError
from rest_framework import six


def dict_raise_on_duplicates(ordered_pairs):
    """
    Reject duplicate keys.
    """
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            raise ValueError("duplicate key: %r" % (k,))
        else:
            d[k] = v
    return d


class JSONStrictParser(BaseParser):
    """
    Parses JSON-serialized data.
    This is an override of rest framework to raise exception
    when a duplicated key is found to fill data.
    We follow the recommendation given in
    http://stackoverflow.com/questions/14902299/json-loads-except-duplicate-keys-in-request
    """

    media_type = 'application/json'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Returns a 2-tuple of `(data, files)`.

        `data` will be an object which is the parsed content of the response.
        `files` will always be `None`.
        """
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            data = stream.read().decode(encoding)
            parsed_json = json.loads(data, object_pairs_hook=dict_raise_on_duplicates)
            if not isinstance(parsed_json, (dict, list)):
                raise ValueError('Invalid JSON type, not array or object')
            return parsed_json
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % six.text_type(exc))
