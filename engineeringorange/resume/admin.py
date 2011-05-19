from django.contrib import admin
from resume.models import Employer,Course,Jobseeker,Announcement

class EmployerAdmin (admin.ModelAdmin):
    list_display = ('companyname','credit')
    search_fields = ('companyname',)
    list_filter = ('industryid',)
    fields = ('companyname','credit')

class JobseekerAdmin (admin.ModelAdmin):
    list_display = ('lastname','gwa','batch')
    search_fields = ('lastname',)
    list_filter = ('courseid',)
    ordering=('lastname',)
    fields = ('courseid','batch','gwa')
    
class AnnouncementAdmin (admin.ModelAdmin):
    list_filter = ('datePosted',)
    date_hierarchy = 'datePosted'
    ordering = ('-datePosted',)
    
class CourseAdmin(admin.ModelAdmin):
    ordering = ('courseid')
    
admin.site.register(Employer,EmployerAdmin)
admin.site.register(Course)
admin.site.register(Jobseeker,JobseekerAdmin)
admin.site.register(Announcement,AnnouncementAdmin)