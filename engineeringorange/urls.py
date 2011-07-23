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
    url(r'^$',views.login),
    url(r'^accounts/login/$',views.login),
    #url(r'^accounts/logout/$',logout),
    url(r'register/',views.register),
    #Jobpost URLS
    url(r'^jobpost/add/(?P<userid>.*)/$', 'engineeringorange.jobposts.views.addpost'),
    url(r'^jobpost/view/(?P<userid>.*)/(?P<jobid>.*)/$', 'engineeringorange.jobposts.views.viewpost'),
    url(r'^jobpost/edit/(?P<userid>.*)/(?P<jobid>.*)/$','engineeringorange.jobposts.views.editpost'),
    url(r'^jobpost/delete/(?P<userid>.*)/(?P<jobid>.*)/$', 'engineeringorange.jobposts.views.deletepost'),
    url(r'^jobpost/searchjobposts/(?P<userid>.*)/$', 'engineeringorange.jobposts.views.searchJobPosts'), 
    url(r'^jobpost/viewsearchresults/(?P<userid>.*)/$', 'engineeringorange.jobposts.views.viewsearchresults'), 
    url(r'^jobpost/(?P<userid>.*)/$', 'engineeringorange.jobposts.views.viewall'),
    
    #Resume URLS    

    url(r'^searchresume/(?P<userid>.*)/$', 'engineeringorange.resume.views.search'),
	url(r'^searcharesume/(?P<userid>.*)/$', 'engineeringorange.resume.views.searchone'),
    url(r'^resume/(?P<userid>.*)/(?P<stdid>.*)/$', 'engineeringorange.resume.views.resume'),
	url(r'^resume/exporttocsv/(?P<courseid>.*)/(?P<batch>.*)/(?P<city>.*)$', 'engineeringorange.resume.views.exporttocsv'),

    #Employer URLS
    url(r'^employer/editaccount/(?P<userid>.*)/$', 'engineeringorange.employer.views.editaccount'),
    url(r'^employer/messages/(?P<userid>.*)/$', 'engineeringorange.messages.views.viewall'),
    url(r'^employer/(?P<userid>.*)/$', 'engineeringorange.employer.views.index'),
    #Message URLS
    url(r'^message/delete/(?P<userid>.*)/(?P<msgid>.*)/$', 'engineeringorange.messages.views.delete'),
    url(r'^messages/sent/(?P<userid>.*)/$', 'engineeringorange.messages.views.sent'),
    url(r'^reply/(?P<userid>.*)/(?P<msgid>.*)/$', 'engineeringorange.messages.views.reply'),
    url(r'^compose/(?P<userid>.*)/$', 'engineeringorange.messages.views.compose'),
    url(r'^message/(?P<userid>.*)/(?P<msgid>.*)/$', 'engineeringorange.messages.views.viewmsg'),
    url(r'^messages/(?P<userid>.*)/$', 'engineeringorange.messages.views.viewall'),
    
    #Jobseeker URLS
    url(r'^jobseeker/editaccount/(?P<userid>.*)/$', 'engineeringorange.jobseeker.views.editaccount'),
    url(r'^jobseeker/messages/(?P<userid>.*)/$', 'engineeringorange.messages.views.viewall'),
    url(r'^jobseeker/searchjobposts/(?P<userid>.*)/$', 'engineeringorange.jobseeker.views.searchJobPosts'),
    url(r'^jobseeker/(?P<userid>.*)/$', 'engineeringorange.jobseeker.views.index'),
    
)