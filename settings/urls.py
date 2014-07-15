from django.conf.urls import patterns, include, url
from genconf.views import GenConfView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'genconf.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', GenConfView.as_view(), name='home'),


    url(r'^admin/', include(admin.site.urls)),
)
