from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from engineeringorange.resume.models import *
import datetime 

# Create your models here.

# Forms Used
class JobseekerForm(ModelForm):
    class Meta:
        model = Jobseeker
        exclude = ('userid', 'gwa')
        
class SearchJobsForm(ModelForm):
    class Meta:
        model = Jobpositions
        fields = ('industryid',)

class JobPostingsForm(ModelForm):
    class Meta:
        model = Jobpostings
        fields = ( 'description',)