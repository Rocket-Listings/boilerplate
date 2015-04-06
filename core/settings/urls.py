from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()
from listings import views as listings
from notifications import views as notifications

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^about/', listings.about, name='about'),
    url(r'^styleguide$', listings.styleguide, name='styleguide'),
    url(r'^api/notifications/viewed', notifications.mark_viewed, name="notifications_mark_viewed"),
    url(r'^$', listings.home, name='home'),


)
