from django.contrib import admin
from resume.models import employer,course,jobseeker,announcement

class EmployerAdmin (admin.ModelAdmin):
    list_display = ('companyName','credit')

class JobseekerAdmin (admin.ModelAdmin):
    list_display = ('userID','gwa','batch')
    
admin.site.register(employer,EmployerAdmin)
admin.site.register(course)
admin.site.register(jobseeker,JobseekerAdmin)
admin.site.register(announcement)