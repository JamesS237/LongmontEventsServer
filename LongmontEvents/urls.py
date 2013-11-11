from django.conf.urls import patterns, include, url
from API import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'LongmontEvents.views.home', name='home'),
    # url(r'^LongmontEvents/', include('LongmontEvents.foo.urls')),

    url(r'^api/getevents/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.getEvents),
    url(r'^api/getevent/(?P<identifier>\d+)/$', views.getEvent),
    url(r'^api/scrapetask/$', views.scrapeCalendars),
    url(r'^api/imgoing/(?P<identifier>\d+)/$', views.processImGoing),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
