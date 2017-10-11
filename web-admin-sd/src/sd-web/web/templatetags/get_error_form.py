"""
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
"""


from django import template
register = template.Library()
@register.filter(name='get_error_form')
def get_error_form(form):

    if len(form.errors) > 0:
        item = form.errors.items()[0]
        message = ':'.join([item[0], item[1][0]])
        return message.replace('__all__:','')
    else:
        return ''