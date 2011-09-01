from engineeringorange.employer.models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def editaccount(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	emp = get_object_or_404(Employer, userid=userid)
	if request.method == "POST":
		form = EmployerForm(request.POST)
		if form.is_valid():
			update = form.save(commit=False)
			update.userid = emp.userid
			update.save()		
			return HttpResponseRedirect('/employer/' +str(update.userid.userid))
	else:
		form = EmployerForm(instance = emp)
	return render_to_response('editemployer.html', {'user': account, 'form': form}, context_instance=RequestContext(request))

@login_required
def index(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	print account.usertype
	if account.usertype == 'employer':
		emp = get_object_or_404(Employer, userid=userid)
		return render_to_response('employer.html', {'employer': emp, 'user': account, 'announcements': Announcement.objects.exclude(annType='j').order_by('datePosted').reverse()})
	if account.usertype == 'jobseeker':
		seeker = get_object_or_404(Jobseeker, userid=userid)
		return render_to_response('jobseeker.html', {'jobseeker': seeker, 'user': account, 'announcements': Announcement.objects.exclude(annType='e').distinct().order_by('datePosted').reverse()})
	return HttpResponseRedirect('/')
