# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from resume.models import Accounts,Jobseeker
from resume.forms import RegistrationForm, LogInForm
import datetime

def login(request):
    if request.method == 'POST':
        loginForm = LogInForm(request.POST)
        if loginForm.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            acc = Accounts.objects.get(userid=username)
            if user is not None and user.is_active:
                auth.login(request, user)
                print('logged')
                if acc.usertype == 'jobseeker':
                    return HttpResponse('jobseeker')
                    #HttpRedirect to jobseeker page here
                else:
                    return HttpResponseRedirect('/employer/'+str(acc.userid)+'/')
                    #HttpRedirect to 'employer' page here
            print('user is not in database or is not active')
    else:
        loginForm = LogInForm()
    return render_to_response('registration/login.html',{'form':loginForm},context_instance=RequestContext(request))

def register (request):
    if request.method == 'POST':
        regForm = RegistrationForm(request.POST)
        if regForm.is_valid():
            user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
            user.first_name = request.POST['firstName']
            user.last_name = request.POST['lastName']
            user.is_active = True
            newAccount = Accounts(userid=request.POST['username'],email=request.POST['email'],usertype='jobseeker',userlink=user)
            newJobseeker = Jobseeker(userid=newAccount,firstname=request.POST['firstName'],lastname=request.POST['lastName'])
            #user.save()
            #newAccount.save()
            #newJobseeker.save()
            #print('hello')
            return HttpResponse("hello user has been created")
    else:
        regForm = RegistrationForm()
    return render_to_response('registration/registration.html',{'form':regForm},context_instance=RequestContext(request))
        