from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from analysis import views

urlpatterns = patterns('',
    url(r'^logout', views.signout),

    url(r'^api/github/repo/(?P<owner>\w+)/(?P<name>\w+)/add', views.add_github_repository),
    url(r'^api/github/repos$', views.github_repos),

    url(r'^api/repos$', views.repos),

    url(r'^api/commit/(?P<commit>\w+)/file/(?P<filename>.+)', views.file_analysis),
    url(r'^api/commit/(?P<commit>\w+)', views.commit_analysis),

    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('social_auth.urls')),

    url(r'^$', views.index, name='index')
)
