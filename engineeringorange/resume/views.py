# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import auth
from resume.models import *
from messages.models import *
from resume.forms import *
import datetime
import random
import csv
from django.contrib.auth.decorators import login_required

def login(request,logout):
    notice = ''
    if request.method == 'POST':
        loginForm = LogInForm(request.POST)
        if loginForm.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            account = Accounts.objects.filter(userid=username).distinct()
            
            if account:
                acc = account[0]
                
            if user is not None and user.is_active:
                auth.login(request, user)
                print('logged')
                if acc.usertype == 'jobseeker':
                    return HttpResponseRedirect('/jobseeker/' + str(acc.userid) + '/')
                    #HttpRedirect to jobseeker page here
                else:
                    return HttpResponseRedirect('/employer/'+str(acc.userid)+'/')
                    #HttpRedirect to 'employer' page here
            elif not account:
                    notice = "User does not exist. Please register now."        
            elif user is None:
                    notice = "Invalid username and password combination"
            else:
                    notice = "User is not active please inform the administration"
    else:
        loginForm = LogInForm()
        if logout:
            notice = "You have successfully logged out"
    return render_to_response('login.html',{'form':loginForm, 'announcements': Announcement.objects.filter(annType='a').order_by('datePosted').reverse(), 'notice': notice, 'notHome':False},context_instance=RequestContext(request))

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
            newAccount.save()
            newJobseeker.save()
            return HttpResponseRedirect("/")
    else:
        regForm = RegistrationForm()
    return render_to_response('registration.html',{'form':regForm},context_instance=RequestContext(request))

def sendpassword(request):
    email = request.GET.get('email', '')
    if email :
        #check if email is in db.
        account = Accounts.objects.filter(email = email)
            
        if account:
            print account    
            try:
                # generate a new password
                result = account[0].userlink
                password = str(random.randint(0,10000000000))
                subject = 'Engineering Orange: Your New Password'
                message = 'The password for your account is: ' + password + '. Please access your account and change the password immediately.'
                print message
                #place new password
                result.set_password(password)
                result.save()
                #send the email
                send_mail(subject, message, 'engineeringorange@gmail.com', [email])
            except BadHeaderError:
                return render_to_response('registration.html',{'forgotpword': 'yup!', 'notice': 'Invalid header found.'})

            return render_to_response('registration.html',{'forgotpword': 'yup!', 'notice': 'Your password has been sent!'})
        else:
            return render_to_response('registration.html',{'forgotpword': 'yup!', 'notice': 'This email hasan\'t been registered. Sign up for an account now!'})    
    return render_to_response('registration.html',{'forgotpword': 'yup!'})

def changepassword(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    form = ChangePasswordForm(request.POST or None)
    notice = ''
    if request.POST and form.is_valid():
        p = str(request.POST['password'])
        new = str(request.POST['newpassword'])
        rep = str(request.POST['repeatpassword'])
        print p
        print new
        print rep
        if account.userlink.check_password(p):
            #check if the new passwords match
            if new == rep:
                #change the password
                print new
                account.userlink.set_password(new)
                account.userlink.save()
                notice = 'Your password has been changed.'
            else:
                notice = 'The New Password and Repeat Password don\'t match.'
        else:
            notice = 'Password typed doesn\'t match the password of this user.'
    return render_to_response('changepassword.html',{'form': form, 'notice': notice, 'user': account}, context_instance=RequestContext(request))

@login_required   
def exporttocsv(request, userid, courseid, batch, city):
    account = get_object_or_404(Accounts, userid=userid)
    if request.POST:
        if courseid or batch or city:
            if courseid != 15:
                qset = (
                    Q(courseid=courseid) | 
                    Q(batch=batch)  |
                    Q(city=city)
	            )
            else:
                qset = (
                    Q(batch=batch) | 
                    Q(city=city)
                )
      	    results = Jobseeker.objects.filter(qset).distinct()
        else:
	    results = []

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=results.csv'
        writer = csv.writer(response)
        writer.writerow(['Lastname', 'Firstname', 'Course', 'Batch', 'Telphone Number', 'Mobile Number', 'Permanent Address'])
        for result in results:
           writer.writerow([result.lastname, result.firstname, result.courseid, result.batch, result.telephonenumber, result.mobilenumber, result.permanentaddress])
        return response
    else:
        return HttpResponseRedirect("/jobpost/" + str(account.userid))

@login_required
def search(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    if account.usertype == 'employer':	
        form = SearchForm(request.POST or None)
        course = request.GET.get('courseid', 0)
        batch = request.GET.get('batch', '')
        city = request.GET.get('city', '')
        if course or batch or city:
            if course != '':
                qset = (
                    Q(courseid=course) | 
                    Q(batch=batch)  |
                    Q(city=city)
	            )
            else:
                qset = (
                    Q(batch=batch) | 
                    Q(city=city)
                )
                course = 15			    
            results = Jobseeker.objects.filter(qset).distinct()
            if city == '':
	            city = 'na'
        else:
	        results = []
        return render_to_response("searchresume.html/", {"user": account, "form": form, "results": results, "course":course, "batch": batch, "city": city},   context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/jobpost/" + str(account.userid))

@login_required
def searchone(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    if account.usertype == 'employer':	
        form = StudentForm(request.POST or None)
    
        last = request.GET.get('lastname')
        first = request.GET.get('firstname')

        if last or first:
            qset = (
                Q(lastname=last) | 
                Q(firstname=first)
            )
            last = first + last
            results = Jobseeker.objects.filter(qset).distinct()
        else:
	    results = []
        return render_to_response("searcharesume.html/", {"user": account, "form": form, "results": results, "query":last},   context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/jobpost/" + str(account.userid))

@login_required	
def resume(request, userid, stdid):
	account = get_object_or_404(Accounts, userid=userid)
	resume = Jobseeker.objects.get(userid=stdid)
	aff = Jsaffiliations.objects.filter(userid=stdid).distinct()
	awards = Jsawards.objects.filter(userid=stdid).distinct()
	education = Jseducation.objects.filter(userid=stdid).distinct()
	employment = Jsemployment.objects.filter(userid=stdid).distinct()
	project = Jsprojects.objects.filter(userid=stdid).distinct()
	seminar = Jsseminars.objects.filter(userid=stdid).distinct()
	form=''
	
	result = Employer.objects.filter(userid=userid).distinct()
	if result:
		form = MessageForm(request.POST or None)
		if request.POST and form.is_valid():
			newmsg = form.save(commit=False)
			newmsg.fromid = account
			newmsg.toid = resume.userid
			newmsg.senddate = datetime.datetime.now()
			newmsg.save()
			return render_to_response("resume.html/", {"user": account, "resume": resume, "aff": aff, "awards":awards, "education": education, "employment": employment, "project": project, "seminar": seminar, "employer": employment, "form": MessageForm(None), "sent": "Your Message has been sent!"},context_instance=RequestContext(request))
	
		return render_to_response("resume.html/", {"user": account, "resume": resume, "aff": aff, "awards":awards, "education": education, "employment": employment, "project": project, "seminar": seminar, "employer": employment, "form": form},context_instance=RequestContext(request))
	if userid == stdid:
		return render_to_response("resume.html/", {"user": account, "resume": resume, "aff": aff, "awards":awards, "education": education, "employment": employment, "project": project, "seminar": seminar, "employer": employment})

	return HttpResponseRedirect('/resume/' + str(account.userid) + '/' + str(account.userid))
