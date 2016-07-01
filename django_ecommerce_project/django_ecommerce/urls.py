from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from payments import views
from main.urls import urlpatterns as main_json_urls
from djangular_polls.urls import urlpatterns as djangular_polls_json_url

admin.autodiscover()
main_json_urls.extend(djangular_polls_json_url)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_ecommerce.views.home', name='home'),
    # url(r'^django_ecommerce/', include('django_ecommerce.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(main_json_urls)),

    url(r'^$', 'main.views.index', name='home'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^contact', 'contact.views.contact', name='contact'),

    # Main
    url(r'^report_status$', 'main.views.report_status', name='report_status'),

    # Django polls urls

    # User registration
    url(r'^sign_in$', views.sign_in, name='sign_in' ),
    url(r'^sign_out$', views.sign_out, name='sign_out' ),
    url(r'^register$', views.register, name='register' ),
    url(r'^edit$', views.edit, name='edit' ),
)
