from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from engineeringorange.resume.models import *
import datetime 

# Create your models here.

class PasswordForm(ModelsForm):
	class Meta:
		model = Accounts
		fields = ('email')
