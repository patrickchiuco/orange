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
    
    #Homepage
    url(r'^$',views.login,{'logout':False}),
    
    #Logging URL's
    url(r'^accounts/login/$',views.login,{'logout':False}),
    url(r'^accounts/logout/$',logout,{'next_page':'login.html'}),
    url(r'accounts/logout/login.html',views.login,{'logout':True}),
    url(r'register/',views.register),
    url(r'resetpassword', views.sendpassword),
    url(r'accounts/changepassword/(?P<userid>.*)/$', views.changepassword),

    #Jobpost URLS
    url(r'^jobpost/add/(?P<userid>.*)/$', 'engineeringorange.jobposts.views.addpost'),
    url(r'^jobpost/view/(?P<userid>.*)/(?P<jobid>.*)/$', 'engineeringorange.jobposts.views.viewpost'),
    url(r'^jobpost/edit/(?P<userid>.*)/(?P<jobid>.*)/$','engineeringorange.jobposts.views.editpost'),
    url(r'^jobpost/delete/(?P<userid>.*)/(?P<jobid>.*)/$', 'engineeringorange.jobposts.views.deletepost'),
    url(r'^jobpost/(?P<userid>.*)/$', 'engineeringorange.jobposts.views.viewall'),

    #Resume URLS
    url(r'^searchresume/(?P<userid>.*)/$', 'engineeringorange.resume.views.search'),
    url(r'^searcharesume/(?P<userid>.*)/$', 'engineeringorange.resume.views.searchone'),
    url(r'^resume/(?P<userid>.*)/(?P<stdid>.*)/$', 'engineeringorange.resume.views.resume'),
    url(r'^resume/exporttocsv/(?P<userid>.*)/(?P<courseid>.*)/(?P<batch>.*)/(?P<city>.*)$', 'engineeringorange.resume.views.exporttocsv'),

    #Employer URLS
    url(r'^employer/editaccount/(?P<userid>.*)/$', 'engineeringorange.employer.views.editaccount'),
    url(r'^employer/(?P<userid>.*)/$', 'engineeringorange.employer.views.index'),

    #Message URLS
    url(r'^message/delete/(?P<userid>.*)/(?P<msgid>.*)/$', 'engineeringorange.messages.views.delete'),
    url(r'^messages/sent/(?P<userid>.*)/$', 'engineeringorange.messages.views.sent'),
    url(r'^reply/(?P<userid>.*)/(?P<msgid>.*)/$', 'engineeringorange.messages.views.reply'),
    url(r'^compose/(?P<userid>.*)/$', 'engineeringorange.messages.views.compose'),
    url(r'^message/(?P<userid>.*)/(?P<msgid>.*)/$', 'engineeringorange.messages.views.viewmsg'),
    url(r'^messages/(?P<userid>.*)/$', 'engineeringorange.messages.views.viewall'),
    
    #Jobseeker URLS
     #EDIT
     url(r'^jobseeker/edit/affiliation/(?P<userid>.*)/(?P<aid>.*)/$', 'engineeringorange.jobseeker.views.editaffiliation'),
     url(r'^jobseeker/edit/award/(?P<userid>.*)/(?P<aid>.*)/$', 'engineeringorange.jobseeker.views.editaward'),
     url(r'^jobseeker/edit/education/(?P<userid>.*)/(?P<educid>.*)/$', 'engineeringorange.jobseeker.views.editeducationbg'),
     url(r'^jobseeker/edit/employment/(?P<userid>.*)/(?P<empid>.*)/$', 'engineeringorange.jobseeker.views.editemployment'),
     url(r'^jobseeker/edit/project/(?P<userid>.*)/(?P<pid>.*)/$', 'engineeringorange.jobseeker.views.editproject'),
     url(r'^jobseeker/edit/seminar/(?P<userid>.*)/(?P<sid>.*)/$', 'engineeringorange.jobseeker.views.editseminar'),

     #DELETE
     url(r'^jobseeker/delete/affiliation/(?P<userid>.*)/(?P<aid>.*)/$', 'engineeringorange.jobseeker.views.deleteaffiliation'),
     url(r'^jobseeker/delete/award/(?P<userid>.*)/(?P<aid>.*)/$', 'engineeringorange.jobseeker.views.deleteaward'),
     url(r'^jobseeker/delete/education/(?P<userid>.*)/(?P<educid>.*)/$', 'engineeringorange.jobseeker.views.deleteeducationbg'),
     url(r'^jobseeker/delete/employment/(?P<userid>.*)/(?P<empid>.*)/$', 'engineeringorange.jobseeker.views.deleteemployment'),
     url(r'^jobseeker/delete/project/(?P<userid>.*)/(?P<pid>.*)/$', 'engineeringorange.jobseeker.views.deleteproject'),
     url(r'^jobseeker/delete/seminar/(?P<userid>.*)/(?P<sid>.*)/$', 'engineeringorange.jobseeker.views.deleteseminar'),

     #ADD
     url(r'^jobseeker/viewall/affiliations/(?P<userid>.*)/$', 'engineeringorange.jobseeker.views.addaffiliation'),
     url(r'^jobseeker/viewall/awards/(?P<userid>.*)/$', 'engineeringorange.jobseeker.views.addaward'),
     url(r'^jobseeker/viewall/education/(?P<userid>.*)/$', 'engineeringorange.jobseeker.views.addeducationbg'),
     url(r'^jobseeker/viewall/employment/(?P<userid>.*)/$', 'engineeringorange.jobseeker.views.addemployment'),
     url(r'^jobseeker/viewall/projects/(?P<userid>.*)/$', 'engineeringorange.jobseeker.views.addproject'),
     url(r'^jobseeker/viewall/seminars/(?P<userid>.*)/$', 'engineeringorange.jobseeker.views.addseminar'),

     #OTHERS
     url(r'^jobseeker/editaccount/(?P<userid>.*)/$', 'engineeringorange.jobseeker.views.editaccount'),
     url(r'^jobseeker/(?P<userid>.*)/$', 'engineeringorange.jobseeker.views.index'),
)
