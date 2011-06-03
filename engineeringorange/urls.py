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
    url(r'register/',views.register)
                        
)
