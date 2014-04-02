from django.conf.urls import patterns, include, url

from django.contrib import admin
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
    url(r'^upload$', 'upload'),
    url(r'^photos$', 'index'),
    url(r'^photos/edit$', 'edit'),
    url(r'^photos/(?P<id>\d+)$', 'show'),
)
