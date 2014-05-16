from django.conf.urls import patterns, include, url
from django.contrib import admin

from photos.views import PhotoList, AlbumList

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'photo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    'django.contrib.auth.views',
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
)

urlpatterns += patterns(
    'core.views',
    url(r'^$', 'root'),
)

urlpatterns += patterns(
    'photos.views',
    url(r'^manage$', 'manage'),
    url(r'^photos$', 'index'),
    url(r'^photos/edit$', 'edit'),
    url(r'^photos/(?P<id>\d+)$', 'show'),
    url(r'^albums/(?P<id>\d+)$', 'album_show'),
    url(r'^api/photos/(?P<id>\d+)$', 'photo_delete'),
)

urlpatterns += patterns(
    '',
    url(r'^api/photos$', PhotoList.as_view()),
)

urlpatterns += patterns(
    '',
    url(r'^api/albums$', AlbumList.as_view()),
    url(r'^api/albums/(?P<pk>[0-9]+)$', AlbumList.as_view())
)
