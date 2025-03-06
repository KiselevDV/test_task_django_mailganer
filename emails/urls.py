from django.conf.urls import url

from emails.views import campaign_page, get_campaigns, create_campaign, track_email_open


urlpatterns = [
    url(r'^$', campaign_page, name='campaign_page'),
    url(r'^create_campaign/$', create_campaign, name='create_campaign'),
    url(r'^get_campaigns/$', get_campaigns, name='get_campaigns'),
    url(r'^track/(?P<subscriber_id>\d+)/$', track_email_open, name='track_email_open'),
]
