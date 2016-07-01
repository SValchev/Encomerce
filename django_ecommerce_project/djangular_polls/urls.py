from django.conf.urls import patterns, url
from . import json_views

urlpatterns = patterns('djangular_polls.views',
                        url(r'^polls/$',json_views.PollCollection.as_view(), name='polls_collection'),
                        url(r'^polls/(?P<pk>[0-9]+)$', json_views.PollMember.as_view()),
                        url(r'^poll_item/$',json_views.PollItemCollection.as_view(), name='poll_item'),
                        url(r'^poll_item/(?P<pk>[0-9]+)$', json_views.PollItemMember),
    )
