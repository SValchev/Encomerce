from django.test import TestCase
from django.test.client import RequestFactory

from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from django.db import IntegrityError

from payments.models import User, UnpadaidUser
from payments.forms import SigninForm, UserForm
from payments.views import sign_in, sign_out, soon, register

#from formtools.tests.wizard.wizardtests.forms import UserForm
import django_ecommerce.settings as settings

import mock
import socket


class ViewTestMixins(object):

    @classmethod
    def setupViewTestr(cls,url, view_func, expected_html, status_code=200, session={}):
        request_factory = RequestFactory()
        cls.request = request_factory.get(url)
        cls.request.session = session
        cls.status_code = status_code

        cls.url=url
        cls.view_func = staticmethod(view_func)
        cls.expected_html = expected_html

    def test_resolce_to_the_correct_view(self):
        test_view = resolve(self.url)
        self.assertEqual(test_view.func, self.view_func)

    def test_status_code_is_right(self):
        response = self.view_func(self.request)
        self.assertEqual(response.status_code, self.status_code)

    def test_returns_right_html(self):
        response = self.view_func(self.request)
        self.assertEqual(response.content, self.expected_html)


class RegisterPageTest(TestCase,ViewTestMixins):
    ##########################
    ## Setups and TearDowns ##
    ##########################
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        html = render_to_response(
            'register.html',
            {
                 'form':UserForm(),
                 'months':list(range(1,12)),
                 'publishable':settings.STRIPE_PUBLISH,
                 'soon':soon(),
                 'user': None,
                 'years':list(range(2011,2036)),
            },
            )

        ViewTestMixins.setupViewTestr('/register', register, html.content)

    def setUp(self):
        request_factory = RequestFactory()
        request = request_factory.get(self.url)

    #####################
    ## Helpr Functions ##
    #####################

    def get_mock_cust():

        class mock_cust():

            @property
            def id(self):
                return 1234

        return mock_cust()

    def get_MockUserFocm(self):

        from django import forms

        class MockUserForm(forms.Forms):

            def is_valid(self):
                return True

            @property
            def cleaned_data(self):
                return {
                    'name':'my_name',
                    'email':'python@mail.bg',
                    'stripe_token':'....',
                    'last_4_digits':'4242',
                    'password':'secret_password',
                    'verify_password':'secret_password',
                }

            def addError(self):
                pass

        return MockUserForm()

    ###########
    ## Tests ##
    ###########
    def test_invalid_form_returns_register_page(self):
        with mock.patch('payments.forms.UserForm.is_valid') as user_mock:
            user_mock.return_value = False
            self.request.method = 'POST'
            self.request.POST = None

            resp = register(self.request)

            self.assertEqual(resp.content, self.expected_html)
            self.assertEqual(user_mock.call_count, 1)

    # def test_register_new_user_succsesfuly(self, create_mock, stripe_mock):
    #     self.request.session = {}
    #     self.request.method = 'POST'
    #
    #     self.request.POST = { 'email':'stanimir@mail.bg',
    #                           'name':'some_name',
    #                           'stripe_token':'...',
    #                           'last_4_digits':'4242',
    #                           'password':'secret_password',
    #                           'verify_password' : 'secret_password' }
    #
    #     with mock.patch('stripe.Customer') as stripe_mock:
    #         config = {'create.return_value': mock.Mock()}
    #         stripe_mock.configure_mock(**config)
    #
    #         resp = register(self.request)
    #         self.assertEqual("", resp.content)
    #         self.assertEqual(resp.status_code, 302)
    #         self.assertEqual(self.request.session['user'],1)


    @mock.patch('payments.views.Customer.create',
                return_value=get_mock_cust())
    def test_register_new_user_return_succesfully(self, stripe_mock):
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'name':'my_name',
            'email':'python@mail.bg',
            'stripe_token':'....',
            'last_4_digits':'4242',
            'password':'secret_password',
            'verify_password':'secret_password',
        }
        resp = register(self.request)

        self.assertEqual(resp.content, b"")
        self.assertEqual(resp.status_code, 302)

        user = User.objects.filter(email="python@mail.bg")

        self.assertEqual(len(user), 1)
        self.assertEqual(user[0].stripe_id, '1234')

    @mock.patch('payments.models.UnpadaidUser.save',
                side_effect=IntegrityError,)
    def test_register_stripe_is_down_all_or_nothing(self, save_mock):
            self.request.session = {}
            self.request.method = 'POST'
            self.request.POST = {
                'name':'my_name',
                'email':'python@mail.bg',
                'stripe_token':'....',
                'last_4_digits':'4242',
                'password':'secret_password',
                'verify_password':'secret_password',
            }

            with mock.patch('stripe.Customer.create', side_effect=socket.error('Can not connect to Stripe')) as stripe_mock:

                resp = register(self.request)

                user = User.objects.filter(email="python@mail.bg")
                self.assertEqual(len(user), 0)

                unpaid_users = UnpadaidUser.objects.filter(email="python@mail.bg")
                self.assertEqual(len(unpaid_users), 1)



    def test_register_when_stripe_is_down(self):
        self.request.session = {}
        self.request.method = 'POST'

        self.request.POST = {
            'email':'stanimir@mail.bg',
            'name':'some_name',
            'stripe_token':'...',
            'last_4_digits':'4242',
            'password':'secret_password',
            'verify_password':'secret_password'
        }

        with mock.patch(
        'stripe.Customer.create',
         side_effect=socket.error("Can't connect to stripe"),
         ) as mock_stripe:

            register(self.request)

            unpaid_users = UnpadaidUser.objects.filter(email='stanimir@mail.bg')

            self.assertEqual(len(unpaid_users), 1)
            self.assertEqual(stripe_token, '')
            self.assertIsNotNone(unpaid_users[0].last_notification)


class SignInPageTest(TestCase, ViewTestMixins):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        html = render_to_response('sign_in.html', {'form': SigninForm(), 'user': None})
        ViewTestMixins.setupViewTestr(url='/sign_in', view_func=sign_in, expected_html=html.content)


class SignOutPageTest(TestCase, ViewTestMixins):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ViewTestMixins.setupViewTestr(
        '/sign_out',
         sign_out,
         b'',
         status_code = 302)

    def setUp(self):
        self.request.session = {'user':'dummy'}
