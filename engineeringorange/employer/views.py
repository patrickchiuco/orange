from engineeringorange.employer.models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, get_object_or_404

# Create your views here.

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

def index(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	emp = get_object_or_404(Employer, userid=userid)
	return render_to_response('employer.html', {'employer': emp, 'user': account, 'announcements': Announcement.objects.filter(annType='e').distinct()[:10]})

def viewall(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	return render_to_response('inbox.html', {'user': account, 'messages': Messages.objects.filter(toid=account).distinct()[:20]})

def viewmsg(request, userid, msgid):
	account = get_object_or_404(Accounts, userid=userid)
	message = get_object_or_404(Messages, msgid=msgid)
	return render_to_response('message.html', {'user': account, 'message': message})
	