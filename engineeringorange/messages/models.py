from engineeringorange.resume.models import *
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from django import forms
import datetime 

#Forms used
class MessageForm(ModelForm):
	class Meta:
		model = Messages
		exclude = ('msgid', 'readdate', 'senddate');
