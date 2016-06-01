"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import index
from django.shortcuts import render_to_response
from django.test import RequestFactory
import mock


class MainPageTests(TestCase):
    ############
    ## Setups ##
    ############
    
    @classmethod
    def setUp(cls):
        request_factory = RequestFactory()
        cls.request = request_factory.get('/')
        cls.request.session={}
    
    ###########
    ## Tests ##
    ###########
    def test_root_resolve_to_main_view(self):
        main_page= resolve('/')
        self.assertEqual(main_page.func, index)
    
    
    def test_return_appririate_html(self):
        main_page = index(self.request)
        self.assertEqual(main_page.status_code, 200)
        
    def test_user_html_template(self):
        main_page = index(self.request)
        self.assertTemplateUsed(main_page, 'index.html')
        
    def test_return_right_html(self):
        main_page = index(self.request)
        self.assertEqual(main_page.content,
                         render_to_response("index.html").content)
        
    def test_user_can_log_in(self):
        from payments.models import User
        
        user = User(name='jj',
                    email='jj@test.com',
                    )
        
        self.request.session = {"user":"1"}
        
        with mock.patch('main.views.User') as user_mock:
            config={'get_user_by_id.return_value':user}
            user_mock.objects.configure_mock(**config)
        
            resp= index(self.request)
        
            self.request.session = {}
            
            self.assertTemplateUsed(resp, 'user.html')