from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from engineeringorange.resume.models import *
import datetime 

# Create your models here.

# Forms Used
class EmployerForm(ModelForm):
	class Meta:
		model = Employer
		exclude = ('userid', 'industryid')
		
