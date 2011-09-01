# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db import models
from django import forms
import datetime 

#Static Tables start here
class Accounts(models.Model):
    userTypeChoices = (
        ('admin','admin'),
        ('employer','employer'),
        ('jobseeker','jobseeker'),
    )
    
    userid = models.CharField(max_length=60, primary_key=True, db_column='userID') # Field name made lowercase.
    usertype = models.CharField(max_length=27, db_column='userType', choices=userTypeChoices, default='jobseeker') # Field name made lowercase.
    email = models.CharField(max_length=120)
    history = models.DateTimeField(default=datetime.datetime.now())
    expiry = models.DateTimeField(null=True, blank=True)
    activation = models.DateTimeField(null=True, blank=True)
    userlink = models.ForeignKey(User,default=0)
    
    class Meta:
        db_table = u'accounts'
    def __unicode__ (self):
        return unicode((self.email))

class Course(models.Model):
    courseid = models.AutoField(primary_key=True, db_column='courseID') # Field name made lowercase.
    title = models.CharField(max_length=240)
    class Meta:
        db_table = u'course'
    def __unicode__ (self):
        return unicode ((self.title))
        
class Industry(models.Model):
    industryid = models.AutoField(primary_key=True, db_column='industryID') # Field name made lowercase.
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    class Meta:
        db_table = u'industry'
    def __unicode__ (self):
        return unicode ((self.title))
        
class Skillcategories(models.Model):
    categoryid = models.AutoField(primary_key=True, db_column='categoryID') # Field name made lowercase.
    title = models.CharField(max_length=90)
    class Meta:
        db_table = u'skillcategories'
    def __unicode__(self):
        return unicode((self.title))
        
class Skills(models.Model):
    skillid = models.AutoField(primary_key=True, db_column='skillID') # Field name made lowercase.
    skill = models.CharField(max_length=120)
    categoryid = models.ForeignKey(Skillcategories, db_column='categoryID') # Field name made lowercase.
    class Meta:
        db_table = u'skills'
    def __unicode__ (self):
        return unicode((self.skill))


class Employer(models.Model):
    userid = models.ForeignKey(Accounts, db_column='userID',primary_key=True) # Field name made lowercase.
    companyname = models.CharField(max_length=120, db_column='companyName') # Field name made lowercase.
    industryid = models.ForeignKey(Industry, db_column='industryID',default=1) # Field name made lowercase.
    address = models.TextField(blank=True,null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    telephonenumber = models.CharField(max_length=60, db_column='telephoneNumber', blank=True, null=True) # Field name made lowercase.
    companylogo = models.FileField(upload_to='company_logos',db_column='companyLogo', blank=True, null=True) # Field name made lowercase.
    infosheet = models.FileField(upload_to='infosheets',db_column='infoSheet', blank=True, null=True) # Field name made lowercase.
    background = models.TextField()
    url = models.CharField(max_length=240, blank=True, null=True)
    credit = models.IntegerField(default=50)
    class Meta:
        db_table = u'employer'
    def __unicode (self):
        return unicode((self.userid,self.companyname))


class Jobpositions(models.Model):
    jobid = models.AutoField(primary_key=True, db_column='jobID') # Field name made lowercase.
    title = models.CharField(max_length=240)
    description = models.TextField()
    industryid = models.ForeignKey(Industry, db_column='industryID') # Field name made lowercase.
    class Meta:
        db_table = u'jobpositions'
    def __unicode__ (self):
        return unicode((self.jobid,self.title))

class Jobpostings(models.Model):
    postid = models.AutoField(primary_key=True, db_column='postID') # Field name made lowercase.
    userid = models.ForeignKey(Accounts, null=True, db_column='userID', blank=True) # Field name made lowercase.
    postdate = models.DateTimeField(db_column='postDate',default='2006-01-01 00:00:00') # Field name made lowercase.
    validity = models.DateTimeField(default='2006-01-01 00:00:00')
    jobid = models.ForeignKey(Jobpositions,db_column='jobID') # Field name made lowercase.
    description = models.TextField(blank=True)
    qualifications = models.TextField(blank=True)
    class Meta:
        db_table = u'jobpostings'
    def __unicode__ (self):
        return unicode((self.postid,self.description))

class Jobseeker(models.Model):
    genderChoices=(
        ('male','male'),
        ('female','female'),
    )
    
    userid = models.ForeignKey(Accounts, db_column='userID', primary_key=True) # Field name made lowercase.
    firstname = models.CharField(max_length=120, db_column='firstName') # Field name made lowercase.
    middlename = models.CharField(max_length=120, db_column='middleName', blank=True) # Field name made lowercase.
    lastname = models.CharField(max_length=120, db_column='lastName', blank=True) # Field name made lowercase.
    courseid = models.ForeignKey(Course, null=True, db_column='courseID', blank=True) # Field name made lowercase.
    gwa = models.FloatField(default=0)
    batch = models.CharField(max_length=30,default=0)
    background = models.TextField()
    presentaddress = models.TextField(db_column='presentAddress', blank=True,null=True) # Field name made lowercase.
    permanentaddress = models.TextField(db_column='permanentAddress') # Field name made lowercase.
    city = models.CharField(max_length=120, blank=True,null=True)
    telephonenumber = models.CharField(max_length=60, db_column='telephoneNumber', blank=True,null=True) # Field name made lowercase.
    mobilenumber = models.CharField(max_length=60, db_column='mobileNumber', blank=True,null=True) # Field name made lowercase.
    #photo = models.FileField(upload_to='js_photos',blank=True,null=True)
    #resume = models.FileField(upload_to='resumes',blank=True,null=True)
    birthday = models.DateField(default='1900-01-01')
    gender = models.CharField(max_length=18,choices=genderChoices,default='male')
    url = models.CharField(max_length=240, blank=True,null=True)
    objective = models.TextField(blank=True)
    jobskills = models.ManyToManyField(Skills, through='Jsskills')
    class Meta:
        db_table = u'jobseeker'
    def __unicode__(self):
        return unicode((self.userid))
    
class Jsskills(models.Model):
    jsskillsid = models.AutoField(primary_key=True)
    jobskills = models.ForeignKey(Jobseeker, db_column='jobskills') # Field name made lowercase.
    skillid = models.ForeignKey(Skills, db_column='skillID') # Field name made lowercase.
    class Meta:
        db_table = u'jsskills'
    def __unicode__(self):
        return unicode((self.userid,self.skillid))

class Jsaffiliations(models.Model):
    userid = models.ForeignKey(Accounts, db_column='userID') # Field name made lowercase.
    organization = models.CharField(max_length=240)
    position = models.CharField(max_length=150)
    startdate = models.DateField(db_column='startDate') # Field name made lowercase.
    enddate = models.DateField(null=True, db_column='endDate', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jsaffiliations'
    def __unicode__(self):
        return unicode((self.userid,self.organization,self.position))

class Jsawards(models.Model):
    userid = models.ForeignKey(Accounts, db_column='userID') # Field name made lowercase.
    institution = models.CharField(max_length=180)
    award = models.CharField(max_length=240)
    datereceived = models.DateField(db_column='dateReceived') # Field name made lowercase.
    class Meta:
        db_table = u'jsawards'
    def __unicode__(self):
        return unicode((self.userid,self.institution,self.award))

class Jseducation(models.Model):
    userid = models.ForeignKey(Accounts, db_column='userID') # Field name made lowercase.
    institution = models.CharField(max_length=180)
    degree = models.CharField(max_length=150)
    startdate = models.DateField(db_column='startDate',default='2006-01-01') # Field name made lowercase.
    enddate = models.DateField(null=True, db_column='endDate', blank=True) # Field name made lowercase.
    honors = models.TextField(blank=True)
    class Meta:
        db_table = u'jseducation'
    def __unicode__(self):
        return unicode((self.userid,self.institution,self.degree))


class Jsemployment(models.Model):
    userid = models.ForeignKey(Accounts, db_column='userID') # Field name made lowercase.
    employer = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    startdate = models.DateField(db_column='startDate',default='2006-01-01') # Field name made lowercase.
    enddate = models.DateField(null=True, db_column='endDate', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jsemployment'
    def __unicode__(self):
        return unicode((self.userid,self.employer,self.position))


class Jsprojects(models.Model):
    userid = models.ForeignKey(Accounts,db_column='userID') # Field name made lowercase.
    title = models.CharField(max_length=300)
    description = models.TextField()
    class Meta:
        db_table = u'jsprojects'
    def __unicode__(self):
        return unicode((self.projectid,self.title))


class Jsseminars(models.Model):
    userid = models.ForeignKey(Accounts, db_column='userID') # Field name made lowercase.
    title = models.CharField(max_length=180)
    startdate = models.DateField(db_column='startDate',default='2006-01-01') # Field name made lowercase.
    enddate = models.DateField(null=True, db_column='endDate', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'jsseminars'
    def __unicode__(self):
        return unicode((self.userid,self.title))



class Messages(models.Model):
    msgid = models.AutoField(primary_key=True, db_column='msgID') # Field name made lowercase.
    fromid = models.ForeignKey(Accounts, null=True, db_column='fromID', blank=True,related_name='fromID') # Field name made lowercase.
    toid = models.ForeignKey(Accounts, null=True, db_column='toID', blank=True,related_name='toID') # Field name made lowercase.
    subject = models.CharField(max_length=90, blank=True)
    message = models.TextField(blank=True)
    senddate = models.DateTimeField(db_column='sendDate',default='2006-01-01') # Field name made lowercase.
    readdate = models.DateTimeField(null=True, db_column='readDate', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'messages'
    def __unicode__(self):
        return unicode((self.msgid,self.subject))


class Settings(models.Model):
    userid = models.ForeignKey(Accounts, db_column='userID',primary_key=True) # Field name made lowercase.
    istelnoviewable = models.BooleanField(db_column='isTelNoViewable') # Field name made lowercase.
    isemailviewable = models.BooleanField(db_column='isEmailViewable') # Field name made lowercase.
    ismobileviewable = models.BooleanField(db_column='isMobileViewable') # Field name made lowercase.
    isgwaviewable = models.BooleanField(db_column='isGWAViewable') # Field name made lowercase.
    isalertactive = models.BooleanField(db_column='isAlertActive') # Field name made lowercase.
    class Meta:
        db_table = u'settings'
		
class Announcement (models.Model):
    types = (
        ('a','all'),
        ('e','employer'),
        ('j','jobseeker'),
    )
    
    annID = models.AutoField(primary_key=True)
    annText = models.TextField()
    datePosted = models.DateTimeField(default=datetime.datetime.now(),blank=True)
    annType = models.CharField(max_length=1,choices=types)
    
    class Meta:
        db_table = u'announcement'
    
    def __unicode__(self):
        return unicode((self.annID,self.annText))

#FORMS
class SearchForm(ModelForm):
	courseid = forms.ModelChoiceField(queryset=Course.objects.all(), label="Course")
	class Meta:
		model = Jobseeker
		fields = ('courseid', 'batch', 'city')

class StudentForm(ModelForm):
	firstname = forms.CharField(label="First Name")
	lastname = forms.CharField(label = "Last Name")
	class Meta:
		model = Jobseeker
		fields = ('firstname', 'lastname')

class AffiliationsForm(ModelForm):
	class Meta:
		model = Jsaffiliations
		exclude = ('userid')

class AwardsForm(ModelForm):
	class Meta:
		model = Jsawards
		exclude = ('userid')

class EmploymentForm(ModelForm):
	class Meta:
		model = Jsemployment
		exclude = ('userid')

class EducationForm(ModelForm):
	class Meta:
		model = Jseducation
		exclude = ('userid')

class SeminarsForm(ModelForm):
	class Meta:
		model = Jsseminars
		exclude = ('userid')

class ProjectForm(ModelForm):
	class Meta:
		model = Jsprojects
		exclude = ('userid')
