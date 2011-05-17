from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class account_details (models.Model):
    userTypeChoices = (
        ('adm','admin'),
        ('jsk','jobseeker'),
        ('emp','employer'),
    )
    userID = models.ForeignKey(User,null=False, max_length=20, primary_key=True)
    userType = models.CharField(null=False, choices=userTypeChoices, max_length=9, default='jsk')
    expiry = models.DateTimeField(null=True)
   
    def __unicode__(self):
        return unicode((self.userID,self.userType,self.activation,self.expiry))
    
class course (models.Model):
    courseID = models.AutoField(null=False, primary_key=True)
    title = models.CharField(null=False, max_length=80,default='')

    def __unicode__(self):
        return unicode((self.title))
    
class industries (models.Model):
    industryID = models.AutoField(null=False,primary_key=True)
    title = models.CharField(null=False,max_length=40,default='')
    description = models.TextField()
    
    def __unicode__(self):
        return unicode((self.title))
    
class skillcategories (models.Model):
    categoryID = models.AutoField(primary_key=True)
    title = models.CharField(null=False, max_length=30,default='')
    
    def __unicode__ (self):
        return unicode((self.title))
    
class skills (models.Model):
    skillID = models.AutoField(null=False, primary_key=True)
    skill = models.CharField(null=False, max_length=40,default='')
    categoryID = models.ForeignKey(skillcategories,null=False,default=0)
    
    def __unicode__(self):
        return unicode((self.skill))
    
class employer (models.Model):
    userID = models.ForeignKey(User,null=False,max_length=20, primary_key=True)
    companyName = models.CharField('name',null=False,max_length=40, default='')
    industryID = models.ForeignKey(industries, verbose_name='industry',null=False)
    address = models.TextField()
    city = models.CharField(max_length=40,null=True)
    telephoneNumber= models.CharField('contact #',max_length=20,null=True)
    #companyLogo = models.FileField(upload_to='company/logo/', blank=True)
    #infoSheet = models.FileField(upload_to='company/infosheet/', blank=True)
    background = models.TextField()
    url = models.CharField(max_length=80,null=True)
    credit = models.IntegerField(max_length=11,default=50)
    
    def __unicode__(self):
        return unicode((self.userID,self.companyName,self.credit))
    
class jobseeker (models.Model):
    genderChoices = (
        ('m','male'),
        ('f','female')
    )
    
    userID = models.ForeignKey(User,null=False,primary_key=True)
    #firstName = models.CharField(max_length=40, null=False,default='')
    #middleName = models.CharField(max_length=40, null=True,default=None)
    #lastName = models.CharField(max_length=40, null=True,default=None)
    courseID = models.ForeignKey(course, verbose_name='course',null=True)
    gwa = models.FloatField('GWA',null=False,default=0)
    batch = models.CharField(max_length=10,default='0')
    background = models.TextField(null=False)
    presentAddress = models.TextField('present Address',null=True)
    permanentAddress = models.TextField('permanent Address',null=False)
    city = models.CharField(max_length=40,null=True,default=None)
    telephoneNumber = models.CharField(max_length=20,null=True,default=None)
    mobileNumber = models.CharField(max_length=20,null=True,default=None)
    #photo = models.FileField(null=True)
    #resume = models.FileField(null=True)
    birthday = models.DateField(null=False,default='1900-01-01')
    gender = models.CharField(max_length=1,null=False,default='m',choices=genderChoices)
    url = models.CharField(null=True,max_length=80,default=None)
    objective = models.TextField(null=True)
    jobskills = models.ManyToManyField(skills,through='jsskills')
    
    def __unicode__(self):
        return unicode((self.userID,self.gwa))
    
class jsskills (models.Model):
    jobskills = models.ForeignKey(jobseeker,primary_key=True)
    skillID = models.ForeignKey(skills)
    
    def __unicode__(self):
        return unicode((self.skills,self.skillID))   

class jobpositions (models.Model):
    jobID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=80,default='')
    description = models.TextField()
    industryID = models.ForeignKey(industries, null=False,default=0)
    
    def __unicode__(self):
        return unicode((self.title,self.description))
    
class jobpostings (models.Model):
    postID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User,null=False,default=None)
    postDate = models.DateTimeField(null=False,default='2006-01-01 00:00:00')
    validity = models.DateTimeField(null=False,default='2006-01-01 00:00:00')
    jobID = models.ForeignKey(jobpositions,null=False,default=0)
    description = models.TextField(null=True)
    qualification = models.TextField(null=True)
    
    def __unicode__(self):
        return unicode((self.postDate,self.validity,self.jobID))
    
    
class jsaffiliations (models.Model):
    userID = models.ForeignKey(User,null=False,primary_key=True,default='')
    organization = models.CharField(max_length=80,null=False,default='')
    position = models.CharField(max_length=50,null=False,default='')
    startDate = models.DateField(null=False,default='2006-01-01')
    endDate = models.DateField(null=True,default=None)
    
    def __unicode__(self):
        return unicode((self.userID,self.organization,self.position))
    
class jsawards (models.Model):
    userID = models.ForeignKey(User,null=False,primary_key=True,default='')
    institution = models.CharField(max_length=60,default='')
    award = models.CharField(max_length=80,default='')
    dateReceived = models.DateField(default='2006-01-01')
    
    def __unicode__ (self):
        return unicode((self.userID,self.institution,self.award))

class jseducation (models.Model):
    userID = models.ForeignKey(User,null=False,primary_key=True,default='')
    institution = models.CharField(max_length=60,null=False,default='')
    degree = models.CharField(max_length=50,null=False,default='')
    startDate = models.DateField(null=False,default='2006-01-01')
    endDate = models.DateField(null=True,default=None)
    honors = models.TextField(null=True,default=None)
    
    def __unicode__(self):
        return unicode((self.userID,self.institution,self.degree))
    
class jsemployment (models.Model):
    userID = models.ForeignKey(User,null=False,primary_key=True,default='')
    employer = models.CharField(max_length=50,null=False,default='')
    position = models.CharField(max_length=50,null=False,default='')
    description = models.TextField(null=True,default=None)
    startDate = models.DateField (null=False,default='2006-01-01')
    endDate = models.DateField(null=True,default=None)
    
    def __unicode__(self):
        return unicode((self.userID,self.employer,self.position))
    
class jsprojects (models.Model):
    projectId = models.AutoField(null=False,primary_key=True)
    userID  = models.ForeignKey(User,null=False)
    title = models.CharField(null=False,max_length=100)
    description = models.TextField(null=False)
    
    def __unicode__ (self):
        return unicode ((self.projectId,self.title))
    
class jsseminars (models.Model):
    userID = models.ForeignKey(User,null=False,primary_key=True,default='')
    title = models.CharField(max_length=60,null=False,default='')
    startDate = models.DateField(null=False,default='2006-01-01')
    endDate = models.DateField(null=True,default=None)
    
    def __unicode__ (self):
        return unicode ((self.userID,self.title))

class settings (models.Model):
    userID = models.ForeignKey(User,null=False,primary_key=True)
    isTelNoViewable = models.BooleanField(default=True)
    isEmailViewable = models.BooleanField(default=True)
    isMobileViewable = models.BooleanField(default=True)
    isGWAViewable = models.BooleanField(default=True)
    isAlertActive = models.BooleanField(default=True)
    
    def __unicode__(self):
        return unicode((self.userID,self.isTelNoViewable,self.isEmailViewable,self.isMobileViewable,self.isGWAViewable,self.isAlertActive))
    
class messages (models.Model):
    fromID = models.ForeignKey(User,null=False,related_name='from')
    toID = models.ForeignKey(User,null=False, related_name='to')
    subject = models.CharField(max_length=30,null=True,default=None)
    message = models.TextField(null=True,default=None)
    sendDate = models.DateTimeField(null=False,default='2006-01-01 00:00:00')
    readDate = models.DateTimeField(null=True,default=None)
    
    def __unicode__(self):
        return unicode((self.fromID,self.toID,self.subject,self.message))
    
class announcement (models.Model):
    annID = models.AutoField(primary_key=True)
    message = models.TextField(null=False)
    date_posted = models.DateTimeField('date Posted',default=datetime.datetime.now(),blank=True)
    
    def __unicode__(self):
        return unicode ((self.message,self.date_posted))
    