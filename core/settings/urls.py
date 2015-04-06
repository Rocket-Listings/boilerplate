from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()
from listings import views as listings

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^about$', listings.about, name='about'),
    url(r'^styleguide$', listings.styleguide, name='styleguide'),
    url(r'^$', listings.home, name='home'),

)
