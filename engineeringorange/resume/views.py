# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib import auth
from resume.models import *
from messages.models import *
from django.db.models import Q
from resume.forms import RegistrationForm, LogInForm
import datetime
import csv

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

def exporttocsv(request, courseid, batch, city):
    print courseid
    print batch
    print city
    if courseid or batch or city:
        print("I got here too!")
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
        print qset
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

def search(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
	
    form = SearchForm(request.POST or None)
    course = request.GET.get('courseid', 0)
    batch = request.GET.get('batch', '')
    city = request.GET.get('city', '')
    if course or batch or city:
        print("I got here!")
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
        print qset
        print city
    	results = Jobseeker.objects.filter(qset).distinct()
        if city == '':
	        city = 'na'
    else:
	    results = []
    return render_to_response("searchresume.html/", {"user": account, "form": form, "results": results, "course":course, "batch": batch, "city": city},   context_instance=RequestContext(request))
 
def searchone(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    form = StudentForm(request.POST or None)
    
    last = request.GET.get('lastname')
    first = request.GET.get('firstname')

    if last or first:
        qset = (
            Q(lastname=last) | 
            Q(firstname=first)
        )
        last = first + last
        print qset
    	results = Jobseeker.objects.filter(qset).distinct()
    else:
	    results = []
    return render_to_response("searcharesume.html/", {"user": account, "form": form, "results": results, "query":last},   context_instance=RequestContext(request))
	
def resume(request, userid, stdid):
	# Get Everything!
	account = get_object_or_404(Accounts, userid=userid)
	resume = Jobseeker.objects.get(userid=stdid)
	aff = Jsaffiliations.objects.filter(userid=stdid).distinct()
	awards = Jsawards.objects.filter(userid=stdid).distinct()
	education = Jseducation.objects.get(userid=stdid)
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
			return render_to_response("resume.html/", {"user": account, "resume": resume, "affliations": aff, "awards":awards, "education": education, "employment": employment, "project": project, "seminar": seminar, "employer": employment, "form": MessageForm(None), "sent": "Your Message has been sent!"},context_instance=RequestContext(request))
		
	return render_to_response("resume.html/", {"user": account, "resume": resume, "affliations": aff, "awards":awards, "education": education, "employment": employment, "project": project, "seminar": seminar, "employer": employment, "form": form},context_instance=RequestContext(request))	
