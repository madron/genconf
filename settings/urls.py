from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext as _

from django.contrib import admin
admin.site.site_header = _('Genconf')
admin.site.site_title = _('Genconf')
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^', include(admin.site.urls)),
)
