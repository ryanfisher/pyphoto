from django.conf.urls import patterns, include, url
from django.contrib import admin

from photos.views import PhotoList, AlbumList

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    'django.contrib.auth.views',
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout', {'next_page': '/photos'}),
)

urlpatterns += patterns(
    'core.views',
    url(r'^$', 'root'),
)

urlpatterns += patterns(
    'photos.views',
    url(r'^manage$', 'manage'),
    url(r'^photos$', 'index'),
    url(r'^photos/(?P<id>\d+)$', 'show'),
    url(r'^albums/(?P<id>\d+)$', 'album_show'),
)

urlpatterns += patterns(
    'profiles.views',
    url(r'^profile/(?P<username>\w+)$', 'show'),
)

urlpatterns += patterns(
    '',
    url(r'^api/photos$', PhotoList.as_view()),
    url(r'^api/photos/(?P<pk>[0-9]+)$', PhotoList.as_view())
)

urlpatterns += patterns(
    '',
    url(r'^api/albums$', AlbumList.as_view()),
    url(r'^api/albums/(?P<pk>[0-9]+)$', AlbumList.as_view())
)
