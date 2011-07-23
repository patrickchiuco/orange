from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login,logout
from resume import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('resume.views',
    # Examples:
    # url(r'^$', 'engineeringorange.views.home', name='home'),
    # url(r'^engineeringorange/', include('engineeringorange.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^media/',),
    #url(r'^$','index'),
)

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':'media'}),
    url(r'^accounts/login/$',views.login),
    #url(r'^accounts/logout/$',logout),
    url(r'register/',views.register),
    url(r'^jobpost/add/(?P<userid>[a-z]*)/$', 'engineeringorange.jobposts.views.addpost'),
    url(r'^jobpost/view/(?P<userid>[a-z]*)/(?P<jobid>\d+)/$', 'engineeringorange.jobposts.views.viewpost'),
    url(r'^jobpost/(?P<userid>[a-z]*)/$', 'engineeringorange.jobposts.views.viewall'),
    url(r'^jobpost/edit/(?P<userid>[a-z]*)/(?P<jobid>\d+)/$','engineeringorange.jobposts.views.editpost'),
    url(r'^jobpost/delete/(?P<userid>[a-z]*)/(?P<jobid>\d+)/$', 'engineeringorange.jobposts.views.deletepost'),
    #Resume URLS
    url(r'^searchresume/(?P<userid>[a-z]*)/$', 'engineeringorange.resume.views.search'),
    url(r'^resume/(?P<userid>[a-z]*)/(?P<stdid>.*)/$', 'engineeringorange.resume.views.resume'),
    #Employer URLS
    url(r'^employer/editaccount/(?P<userid>[a-z]*)/$', 'engineeringorange.employer.views.editaccount'),
    url(r'^employer/messages/(?P<userid>[a-z]*)/$', 'engineeringorange.employer.views.viewall'),
    url(r'^employer/(?P<userid>[a-z]*)/$', 'engineeringorange.employer.views.index'),
    #Message URLS
    url(r'^employer/message/(?P<userid>[a-z]*)/(?P<msgid>\d+)/$', 'engineeringorange.employer.views.viewmsg'),
                        
)
