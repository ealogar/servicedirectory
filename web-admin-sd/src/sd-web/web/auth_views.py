'''
(c) Copyright 2013 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''

from django.contrib.auth import REDIRECT_FIELD_NAME, login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.generic import View, RedirectView
from django.views.generic.edit import FormView
from django.conf import settings


class LoginView(FormView):
    """
    This is a class based version of django.contrib.auth.views.login.
    """
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'login.html'
    success_url = settings.LOGIN_REDIRECT_URL

    @never_cache
    def dispatch(self, *args, **kwargs):

        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        As we are using the AuthenticationForm, it has already validate the user using the "is_valid()" method. The user
        will be validate using the AUTHENTICATION_BACKENDS configured in settings.
        """
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Overrides django.views.generic.edit.ProcessFormView.get() adding a test_cookie to know if the user's browser
        supports cookies
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Overrides django.views.generic.edit.ProcessFormView.post() checking test cookie and deleting it.
        """
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            # TODO: return an error if the cookies are disabled
            self.check_and_delete_test_cookie()
            return self.form_valid(form)
        else:
            self.set_test_cookie()
            return self.form_invalid(form)


class LogoutView(View):
    success_url = settings.LOGOUT_REDIRECT_URL

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(self.success_url)