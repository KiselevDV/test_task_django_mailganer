from django.conf.urls import url

from emails.views import create_campaign, campaign_page, track_email_open


urlpatterns = [
    url(r'^$', campaign_page, name='campaign_page'),
    url(r'^create_campaign/$', create_campaign, name='create_campaign'),
    url(r'^track/(?P<subscriber_id>\d+)/$', track_email_open, name='track_email_open'),
]
