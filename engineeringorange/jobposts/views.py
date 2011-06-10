from engineeringorange.jobposts.models import *
from engineeringorange.messages.models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, get_object_or_404
import datetime

def addpost(request, userid):
	form = JobPositionForm(request.POST or None)
	form2 = JobPostForm(request.POST or None, initial={'validity': datetime.datetime.now()})
	account = get_object_or_404(Accounts, userid=userid)
	
	if request.POST and form.is_valid() and form2.is_valid(): 
			newpos = form.save()
			newpost = form2.save(commit=False)
			position = get_object_or_404(Jobpositions, jobid=newpos.jobid)
			newpost.userid = account
			newpost.jobid = position 
			newpost.description = position.description
			newpost.save()
			return HttpResponseRedirect('/jobpost/view/' + str(account.userid) +'/' +str(newpos.jobid)) # Redirect after POST
			
	return render_to_response('addjob.html/', {'form': form, 'form2': form2, 'user' : account}, context_instance=RequestContext(request))

def deletepost(request, userid, jobid):
	account = get_object_or_404(Accounts, userid=userid)
	position = get_object_or_404(Jobpositions, jobid=jobid)
	posting =  get_object_or_404(Jobpostings, jobid=jobid)
	position.delete()
	posting.delete()
	return HttpResponseRedirect('/jobpost/' + str(account.userid))

	
def editpost(request, userid, jobid):
	account = get_object_or_404(Accounts, userid=userid)
	position = get_object_or_404(Jobpositions, jobid=jobid)
	posting =  get_object_or_404(Jobpostings, jobid=jobid)
	if request.method == "POST":
		form = JobPositionForm(request.POST)
		form2 = JobPostForm(request.POST)
		if form.is_valid() and form2.is_valid():
			position.delete()
			posting.delete()
			newpos = form.save()
			newpost = form2.save(commit=False)
			pos = get_object_or_404(Jobpositions, jobid=newpos.jobid)
			newpost.userid = account
			newpost.jobid = pos
			newpost.description = pos.description
			newpost.save()
			return HttpResponseRedirect('/jobpost/view/' + str(account.userid) +'/'+ str(newpos.jobid))
	else:
		form = JobPositionForm(instance = position)
		form2 = JobPostForm(instance = posting)
	return render_to_response('addjob.html', {'user': account, 'form': form, 'form2': form2}, context_instance=RequestContext(request))
	
def viewpost(request, userid, jobid):
	account = get_object_or_404(Accounts, userid=userid)
	post = get_object_or_404(Jobpostings, jobid=jobid)
	company = get_object_or_404(Employer, userid = post.userid)
	form=''
	
	#check who's viewing the post
	result = Jobseeker.objects.filter(userid=userid).distinct()
	if result:
		form = MessageForm(request.POST or None, initial={'fromid': account, 'toid': post.userid})
		if request.POST and form.is_valid():
			newmsg = form.save(commit=False)
			newmsg.senddate = datetime.datetime.now()
			newmsg.save()
			return HttpResponseRedirect('/message/'+ str(account.userid) +'/' +str(newmsg.msgid))
	
	return render_to_response('viewpost.html', {'user': account, 'post': get_object_or_404(Jobpositions, jobid=jobid), 'qualifications' : post, 'form': form, 'company': company}, context_instance=RequestContext(request))

def viewall(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	return render_to_response('viewallpost.html', {'user' : account, 'posts': Jobpostings.objects.filter(userid=userid).distinct()})
