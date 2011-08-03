from engineeringorange.resume.models import *
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from django import forms
import datetime 

#Forms used - edit para hindi dropdown yung from and to sa message form
class MessageForm(ModelForm):
	class Meta:
		model = Messages
		exclude = ('fromid', 'toid', 'msgid', 'readdate', 'senddate');

class SeekerMessageForm(ModelForm):
	toid = forms.ModelChoiceField(queryset=Accounts.objects.filter(usertype='employer').distinct(), label="To")
	class Meta:
		model = Messages
		exclude = ('fromid', 'msgid', 'readdate', 'senddate');

class EmployerMessageForm(forms.ModelForm):
	toid = forms.ModelChoiceField(queryset=Accounts.objects.filter(usertype='jobseeker').distinct(), label="To")
	class Meta:
		model = Messages
		exclude = ('fromid', 'msgid', 'readdate', 'senddate');

