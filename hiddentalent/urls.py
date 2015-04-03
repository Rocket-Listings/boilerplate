from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^about$', 'hiddentalent.views.about', name='about'),
    url(r'^styleguide$', 'hiddentalent.views.styleguide', name='styleguide'),
    url(r'^$', 'hiddentalent.views.home', name='home'),

)
