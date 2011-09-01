from engineeringorange.jobseeker.models import *
from engineeringorange.resume.models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, get_object_or_404

# Create your views here.

def editaccount(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    js = get_object_or_404(Jobseeker, userid=userid)
    if request.method == "POST":
        form = JobseekerForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.userid = js.userid
            update.save()        
            return HttpResponseRedirect('/jobseeker/' +str(update.userid.userid))
    else:
        form = JobseekerForm(instance = js)
    return render_to_response('editjobseeker.html', {'user': account, 'form': form}, context_instance=RequestContext(request))

def index(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    js = get_object_or_404(Jobseeker, userid=userid)
    if js:
        return render_to_response('jobseeker.html', {'jobseeker': js, 'user': account, 'announcements': Announcement.objects.exclude(annType='e').distinct().order_by('datePosted').reverse()})
    return render_to_response('employer.html', {'jobseeker': js, 'user': account, 'announcements': Announcement.objects.exclude(annType='j').distinct().order_by('datePosted').reverse()})


# edit resume stuff
#Education
def addeducationbg(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    educbg = Jseducation.objects.filter(userid=userid)
    form = EducationForm(request.POST or None)
    if request.POST and form.is_valid():
        update = form.save(commit=False)
        update.userid = account
        update.save()        
        return render_to_response('viewall.html', {'user': account, 'education': educbg, 'field': 'Educational Background', 'form': EducationForm(None)}, context_instance=RequestContext(request))
    return render_to_response('viewall.html', {'user': account, 'education': educbg, 'field': 'Educational Background', 'form': form}, context_instance=RequestContext(request))

def editeducationbg(request, userid, educid):
    account = get_object_or_404(Accounts, userid=userid)
    educbg = get_object_or_404(Jseducation, id = educid)
    if account== educbg.userid: 
	    if request.method == "POST":
		form = EducationForm(request.POST)
		if form.is_valid():
                    educbg.delete()
		    update = form.save(commit=False)
		    update.userid = educbg.userid
		    update.save()        
		    return HttpResponseRedirect('/jobseeker/viewall/education/' +str(update.userid.userid))
	    else:
		form = EducationForm(instance = educbg)
	    return render_to_response('editresume.html', {'user': account, 'education': educbg, 'field': 'Educational Background','form': form}, context_instance=RequestContext(request))
    return HttpResponseRedirect('/jobseeker/viewall/education' + str(account.userid))

def deleteeducationbg(request, userid, educid):
	account = get_object_or_404(Accounts, userid=userid)		
	if request.POST:
		educbg = get_object_or_404(Jseducation, id = educid)
		if account == educbg.userid:
			educbg.delete()
			return HttpResponseRedirect('/jobseeker/viewall/education/' + str(account.userid))
	return HttpResponseRedirect('../#/')

#Employment History
def addemployment(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    employment = Jsemployment.objects.filter(userid=userid)
    form = EmploymentForm(request.POST or None)
    if request.POST and form.is_valid():
        update = form.save(commit=False)
        update.userid = account
        update.save()        
        return render_to_response('viewall.html', {'user': account, 'employment': employment, 'field': 'Employment History', 'form': EmploymentForm(None)}, context_instance=RequestContext(request))
    return render_to_response('viewall.html', {'user': account, 'employment': employment, 'field': 'Employment History', 'form': form}, context_instance=RequestContext(request))

def editemployment(request, userid, empid):
    account = get_object_or_404(Accounts, userid=userid)
    employment = get_object_or_404(Jsemployment, id = empid)
    if account== employment.userid: 
	    if request.method == "POST":
		form = EmploymentForm(request.POST)
		if form.is_valid():
                    employment.delete()
		    update = form.save(commit=False)
		    update.userid = employment.userid
		    update.save()
		    return HttpResponseRedirect('/jobseeker/viewall/employment/' +str(update.userid.userid))
	    else:
		form = EmploymentForm(instance = employment)
	    return render_to_response('editresume.html', {'user': account, 'employment': employment, 'field': 'Employment History', 'form': form}, context_instance=RequestContext(request))
    return HttpResponseRedirect('/jobseeker/viewall/employment/' + str(account.userid))

def deleteemployment(request, userid, empid):
	account = get_object_or_404(Accounts, userid=userid)		
	if request.POST:
		employment = get_object_or_404(Jsemployment, id = empid)
		if account == employment.userid:
			employment.delete()
			return HttpResponseRedirect('/jobseeker/viewall/employment/' + str(account.userid))
	return HttpResponseRedirect('../#/')

#Projects
def addproject(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    projects = Jsprojects.objects.filter(userid=userid)
    form = ProjectForm(request.POST or None)
    if request.POST and form.is_valid():
        update = form.save(commit=False)
        update.userid = account
        update.save()        
        return render_to_response('viewall.html', {'user': account, 'projects': projects, 'field': 'Projects', 'form': ProjectForm(None)}, context_instance=RequestContext(request))
    return render_to_response('viewall.html', {'user': account, 'projects': projects, 'field': 'Projects', 'form': form}, context_instance=RequestContext(request))

def editproject(request, userid, pid):
    account = get_object_or_404(Accounts, userid=userid)
    project = get_object_or_404(Jsprojects, id = pid)
    if account== project.userid: 
	    if request.method == "POST":
		form = ProjectForm(request.POST)
		if form.is_valid():
                    project.delete()
		    update = form.save(commit=False)
		    update.userid = project.userid
		    update.save()
		    return HttpResponseRedirect('/jobseeker/viewall/projects/' +str(update.userid.userid))
	    else:
		form = ProjectForm(instance = project)
	    return render_to_response('editresume.html', {'user': account, 'project': project, 'field': 'Project', 'form': form}, context_instance=RequestContext(request))
    return HttpResponseRedirect('/jobseeker/viewall/projects/' + str(account.userid))

def deleteproject(request, userid, pid):
	account = get_object_or_404(Accounts, userid=userid)		
	if request.POST:
		project = get_object_or_404(Jsprojects, id = pid)
		if account == project.userid:
			project.delete()
			return HttpResponseRedirect('/jobseeker/viewall/projects/' + str(account.userid))
	return HttpResponseRedirect('../#/')

#Affiliations
def addaffiliation(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    affiliations = Jsaffiliations.objects.filter(userid=userid)
    form = AffiliationsForm(request.POST or None)
    if request.POST and form.is_valid():
        update = form.save(commit=False)
        update.userid = account
        update.save()        
        return render_to_response('viewall.html', {'user': account, 'aff': affiliations, 'field': 'Affiliations', 'form': AffiliationsForm(None)}, context_instance=RequestContext(request))
    print affiliations
    return render_to_response('viewall.html', {'user': account, 'aff': affiliations, 'field': 'Affiliations', 'form': form}, context_instance=RequestContext(request))

def editaffiliation(request, userid, aid):
    account = get_object_or_404(Accounts, userid=userid)
    aff = get_object_or_404(Jsaffiliations, id = aid)
    if account== aff.userid: 
	    if request.method == "POST":
		form = AffiliationsForm(request.POST)
		if form.is_valid():
                    aff.delete()
		    update = form.save(commit=False)
		    update.userid = aff.userid
		    update.save()
		    return HttpResponseRedirect('/jobseeker/viewall/affiliations/' +str(update.userid.userid))
	    else:
		form = AffiliationsForm(instance = aff)
	    return render_to_response('editresume.html', {'user': account, 'aff': aff, 'field': 'Affiliation', 'form': form}, context_instance=RequestContext(request))
    return HttpResponseRedirect('/jobseeker/viewall/affiliations/' + str(account.userid))

def deleteaffiliation(request, userid, aid):
	account = get_object_or_404(Accounts, userid=userid)		
	if request.POST:
		aff = get_object_or_404(Jsaffiliations, id = aid)
		if account == aff.userid:
			aff.delete()
			return HttpResponseRedirect('/jobseeker/viewall/affiliations/' + str(account.userid))
	return HttpResponseRedirect('../#/')

#Awards
def addaward(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    awards = Jsawards.objects.filter(userid=userid)
    form = AwardsForm(request.POST or None)
    if request.POST and form.is_valid():
        update = form.save(commit=False)
        update.userid = account
        update.save()        
        return render_to_response('viewall.html', {'user': account, 'awards': awards, 'field': 'Awards', 'form': AwardsForm(None)}, context_instance=RequestContext(request))
    return render_to_response('viewall.html', {'user': account, 'awards': awards, 'field': 'Awards', 'form': form}, context_instance=RequestContext(request))

def editaward(request, userid, aid):
    account = get_object_or_404(Accounts, userid=userid)
    award = get_object_or_404(Jsawards, id = aid)
    if account== award.userid: 
	    if request.method == "POST":
		form = AwardsForm(request.POST)
		if form.is_valid():
                    award.delete()
		    update = form.save(commit=False)
		    update.userid = award.userid
		    update.save()
		    return HttpResponseRedirect('/jobseeker/viewall/awards/' +str(update.userid.userid))
	    else:
		form = AwardsForm(instance = award)
	    return render_to_response('editresume.html', {'user': account, 'award': award, 'field': 'Award Details', 'form': form}, context_instance=RequestContext(request))
    return HttpResponseRedirect('/jobseeker/viewall/awards/' + str(account.userid))

def deleteaward(request, userid, aid):
	account = get_object_or_404(Accounts, userid=userid)		
	if request.POST:
		award = get_object_or_404(Jsawards, id = aid)
		if account == award.userid:
			award.delete()
			return HttpResponseRedirect('/jobseeker/viewall/awards/' + str(account.userid))
	return HttpResponseRedirect('../#/')

#Seminars Attended
def addseminar(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    seminars = Jsseminars.objects.filter(userid=userid)
    form = SeminarsForm(request.POST or None)
    if request.POST and form.is_valid():
        update = form.save(commit=False)
        update.userid = account
        update.save()        
        return render_to_response('viewall.html', {'user': account, 'seminars': seminars, 'field': 'Seminars Attended', 'form': SeminarsForm(None)}, context_instance=RequestContext(request))
    return render_to_response('viewall.html', {'user': account, 'seminars': seminars, 'field': 'Seminars Attended', 'form': form}, context_instance=RequestContext(request))

def editseminar(request, userid, sid):
    account = get_object_or_404(Accounts, userid=userid)
    seminar = get_object_or_404(Jsseminars, id = sid)
    if account== seminar.userid: 
	    if request.method == "POST":
		form = SeminarsForm(request.POST)
		if form.is_valid():
                    seminar.delete()
		    update = form.save(commit=False)
		    update.userid = seminar.userid
		    update.save()
		    return HttpResponseRedirect('/jobseeker/viewall/seminars/' +str(update.userid.userid))
	    else:
		form = SeminarsForm(instance = seminar)
	    return render_to_response('editresume.html', {'user': account, 'seminar': seminar, 'field': 'Seminar Details', 'form': form}, context_instance=RequestContext(request))
    return HttpResponseRedirect('/jobseeker/viewall/seminars/' + str(account.userid))

def deleteseminar(request, userid, sid):
	account = get_object_or_404(Accounts, userid=userid)		
	if request.POST:
		seminar = get_object_or_404(Jsseminars, id = sid)
		if account == seminar.userid:
			seminar.delete()
			return HttpResponseRedirect('/jobseeker/viewall/seminars/' + str(account.userid))
	return HttpResponseRedirect('../#/')

