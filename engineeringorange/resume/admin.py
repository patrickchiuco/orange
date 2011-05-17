from django.contrib import admin
from resume.models import employer,course,jobseeker,announcement

class EmployerAdmin (admin.ModelAdmin):
    list_display = ('companyName','credit')
    search_fields = ('companyName',)
    list_filter = ('industryID',)
    fields = ('companyName','credit')

class JobseekerAdmin (admin.ModelAdmin):
    list_display = ('userID','gwa','batch')
    search_fields = ('userID',)
    list_filter = ('courseID',)
    fields = ('courseID','batch','gwa')
    
class AnnouncementAdmin (admin.ModelAdmin):
    list_filter = ('date_posted',)
    date_hierarchy = 'date_posted'
    ordering = ('-date_posted',)
    
admin.site.register(employer,EmployerAdmin)
admin.site.register(course)
admin.site.register(jobseeker,JobseekerAdmin)
admin.site.register(announcement,AnnouncementAdmin)