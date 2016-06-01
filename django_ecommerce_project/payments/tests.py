"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""


from django.test import TestCase
from django.test.client import RequestFactory

from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response

from payments.models import User
from payments.forms import SigninForm
from payments.views import sign_in, sign_out, soon, register

from django.contrib.formtools.tests.wizard.wizardtests.forms import UserForm
import django_ecommerce.settings as settings

import mock

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
    @classmethod
    def setUpClass(cls):
        html = render_to_response(
            'register.html',
            {
             'form':UserForm(),
             'months':range(1,12),
             'publishable':settings.STRIPE_PUBLISH,
             'soon':soon(),
             'user': None,
             'years':range(2011,2036),
            },)
        
        ViewTestMixins.setupViewTestr('/register', register, html.content)
        
    def setUp(self):
        request_factory = RequestFactory()
        request = request_factory.get(self.url)
        
    def test_invalid_form_returns_register_page(self):
        with mock.patch('payments.forms.UserForm.is_valid') as user_mock:
            user_mock.return_value = False
            self.request.method = 'POST'
            self.request.POST = None
        
            resp = register(self.request)
      
            self.assertEquals(resp.content, self.expected_html)
            self.assertEqual(user_mock.call_count, 1)
            
    def test_register_new_user_succsesfuly(self):
        self.request.session = {}
        self.request.method = 'POST'
        
        self.request.POST = { 'email':'stanimir@mail.bg',
                              'name':'some_name',
                              'stripe_id':'...',
                              'last_4_digits':'4242',
                              'password':'secret_password',
                              'verify_password' : 'secret_password' }
        
        with mock.patch('stripe.Customer') as stripe_mock:
            config = {'create.return_value': mock.Mock()}
            stripe_mock.configure_mock(**config)
            
            resp = register(self.request)
            self.assertEquals("", resp.content)
            self.assertEquals(resp.status_code, 302)
            self.assertEquals(self.request.session['user'],1)
            
    @mock.patch('stripe.Customer.create')
    @mock.patch.object(User, 'create')
    def test_register_new_user_return_succesfully(self, create_mock, stripe_mock):
        self.request.session = {} 
        self.request.method = 'POST'
        self.request.POST = {
                             'email':'python@mail.bg',
                             'name':'my_name',
                             'stripe_id':'....',
                             'last_4_digits':'4242',
                             'password':'secret_password',
                             'verify_password':'secret_password',
        }                            
    
        new_user = create_mock.return_value
        new_cust = stripe_mock.return_value
        
        resp = register(self.request)
        
        self.assertEquals(resp.content, "")
        self.assertEquals(resp.status_code, 302)
        self.assertEquals(self.request.session['user'], new_user.pk)
    
    
    
    
    
    
    
    
        
class SignInPageTest(TestCase, ViewTestMixins): 
    
    @classmethod
    def setUpClass(cls):
        html = render_to_response('sign_in.html', {'form': SigninForm(), 'user': None})
        ViewTestMixins.setupViewTestr(url='/sign_in', view_func=sign_in, expected_html=html.content)
    
    
class SignOutPageTest(TestCase, ViewTestMixins):
    
    @classmethod
    def setUpClass(cls):
        ViewTestMixins.setupViewTestr('/sign_out', sign_out, '', status_code = 302)
        
    def setUp(self):
        self.request.session = {'user':'dummy'}


class FormTestrMixin():
    def assertFormatError(self,form_cls,exptected_error_name,exptected_error_message,data):
        form = form_cls(data=data)
        from pprint import pformat
        
        
        self.assertFalse(form.isvalid())
        self.assertEquals(
            form.errors[exptected_error_name],
            exptected_error_message,
            msg = "Expected {} : Actual {} : using data {}".format(form.errors[exptected_error_message],exptected_error_message, pformat(data))            )


class UserModelsTests(TestCase):
    
    EMAIL_DEFAULT = "new@mail.bg"
    
    @classmethod
    def setUp(cls):
        cls.test_user = User(name="Username", email=cls.EMAIL_DEFAULT)
        cls.test_user.save()
        
    def test_user_to_string_return_email(self):
        self.assertEquals(str(self.test_user), self.EMAIL_DEFAULT)
        
    def test_get_user_by_id(self):
        self.assertEquals(User.get_user_by_id(1), self.test_user)
        
    def test_create_user_stores_in_data(self):
        new_user =  User.create(name="dummy", email="dummy@mail.bg", last_4_digits="4444", stripe_id="22", password="secret_password")
        self.assertEquals(User.objects.get(email="dummy@mail.bg"), new_user)
        
    def test_user_allready_exist_throw_Intergrity_Error(self):
        from django.db import IntegrityError
        self.assertRaises(IntegrityError, User.create,"Username", self.EMAIL_DEFAULT, "4444", "22", "secret_password")
        
        

    
    
    
    
    
    
    