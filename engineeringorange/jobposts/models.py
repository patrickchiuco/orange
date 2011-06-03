from django.contrib.auth.models import User
from django.db import models
from engineeringorange.resume.models import *
from django.forms import ModelForm
import datetime

#Forms used
class JobPostForm(ModelForm):
	class Meta:
		model = Jobpostings
		exclude = ('postid', 'userid', 'jobid', 'postdate','description')

class JobPositionForm(ModelForm):
	class Meta:
		model = Jobpositions
		exclude = ('jobid')