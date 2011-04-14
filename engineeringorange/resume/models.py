from django.db import models

# Create your models here.
class accounts (models.Model):
    userTypeChoices = (
        ('adm','admin'),
        ('jsk','jobseeker'),
        ('emp','employer'),
    )
    userID = models.CharField(null=False, max_length=20, primary_key=True)
    password = models.CharField(null=False, max_length=20)
    userType = models.CharField(null=False, choices=userTypeChoices, max_length=9, default='jsk')
    email = models.CharField(null=False, max_length=40)
    history = models.DateTimeField(null=True)
    expiry = models.DateTimeField(null=True)
    activation = models.DateTimeField(null=True)
    
    def __unicode__(self):
        return unicode((self.userID,self.userType,self.activation,self.expiry))
    
    
class courses (models.Model):
    title = models.CharField(null=False, max_length=80)
    
    def __unicode__(self):
        return unicode((self.title))
    
class industries (models.Model):
    title = models.CharField(null=False,max_length=40)
    description = models.TextField()
    
    def __unicode__(self):
        return unicode((self.title))

class employers (models.Model):
    userID = models.CharField(null=False,max_length=20, primary_key=True)
    companyName = models.CharField(null=False,max_length=40)
    industryID = models.ForeignKey(industries, null=False)
    address = models.TextField()
    city = models.CharField(max_length=40)
    telephoneNumber= models.CharField(max_length=20)
    #companyLogo
    #infoSheet
    background = models.TextField()
    url = models.CharField(max_length=80)
    credit = models.IntegerField(max_length=11)
    
