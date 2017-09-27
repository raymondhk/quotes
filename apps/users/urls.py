from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', indexredirect),
    url(r'^main/$', main),
    url(r'^register/$', register),
    url(r'^login/$', login),
    url(r'^quotes/$', quotes),
    url(r'^process/$', process),
    url(r'^logout/$', logout),
    url(r'^join/(?P<id>\d+)/$', join),
    url(r'^remove/(?P<id>\d+)/$', remove),
    url(r'^user/(?P<id>\d+)/$', user),
]