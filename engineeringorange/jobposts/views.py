from engineeringorange.jobposts.models import *
from engineeringorange.messages.models import *
from django.db.models import Q
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, get_object_or_404
import datetime

@login_required
def addpost(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	if account.usertype == 'employer':
		form = JobPositionForm(request.POST or None)
		form2 = JobPostForm(request.POST or None, initial={'validity': datetime.datetime.now()+datetime.timedelta(days=7)})
	
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
	return HttpResponseRedirect('/jobpost/' + str(account.userid))

@login_required	
def deletepost(request, userid, jobid):
	account = get_object_or_404(Accounts, userid=userid)		
	if request.POST:
		position = get_object_or_404(Jobpositions, jobid=jobid)
		posting =  get_object_or_404(Jobpostings, jobid=jobid)
		position.delete()
		posting.delete()
		return HttpResponseRedirect('/jobpost/' + str(account.userid))
	return HttpResponseRedirect('/jobpost/' + str(account.userid))
	
@login_required
def editpost(request, userid, jobid):
	account = get_object_or_404(Accounts, userid=userid)
	position = get_object_or_404(Jobpositions, jobid=jobid)
	posting =  get_object_or_404(Jobpostings, jobid=jobid)
	
	if posting.userid.userid == account.userid:
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
	return HttpResponseRedirect('/jobpost/' + str(account.userid))

@login_required	
def viewpost(request, userid, jobid):
	account = get_object_or_404(Accounts, userid=userid)
	post = get_object_or_404(Jobpostings, jobid=jobid)
	company = get_object_or_404(Employer, userid = post.userid)
	form=''
	closed=''

	#check is post has expired
	if post.validity < datetime.datetime.now():
		closed = 'this post is closed';	

	#check who's viewing the post
	result = Jobseeker.objects.filter(userid=userid).distinct()
	print request.method
	if result:
		form = MessageForm(request.POST or None, initial={'subject': 'Re: ' + str(post.jobid.title)})
		if request.POST and form.is_valid():
			newmsg = form.save(commit=False)
			newmsg.fromid = account
			newmsg.toid = get_object_or_404(Accounts, email = company.userid)
			newmsg.senddate = datetime.datetime.now()
			newmsg.save()
			return render_to_response('viewpost.html', {'user': account, 'post': get_object_or_404(Jobpositions, jobid=jobid), 'qualifications' : post, 'form': MessageForm( None), 'company': company, 'closed': closed, 'sent': 'Your message has been sent!'}, context_instance=RequestContext(request))
		
		return render_to_response('viewpost.html', {'user': account, 'post': get_object_or_404(Jobpositions, jobid=jobid), 'qualifications' : post, 'form': MessageForm( None), 'company': company, 'closed': closed}, context_instance=RequestContext(request))
	else:
		if account.userid == post.userid.userid:
			return render_to_response('viewpost.html', {'user': account, 'post': get_object_or_404(Jobpositions, jobid=jobid), 'qualifications' : post, 'form': form, 'company': company, 'closed': closed}, context_instance=RequestContext(request))
	
		return HttpResponseRedirect('/jobpost/' + str(account.userid))

@login_required
def viewall(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	if account.usertype == 'employer':
		posts =  Jobpostings.objects.filter(userid=userid).distinct()
	else:
		posts =  Jobpostings.objects.all().distinct()		
	title = request.GET.get('title', '')
	if title:
		qset = (
			Q(description__icontains=title)
		    )
		posts = posts.filter(qset).distinct()

	if account.usertype == 'employer':
		deleteButton = BlankMessageForm(request.POST or None)
		return render_to_response('viewallpost.html', {'user' : account, 'posts':posts, 'delete': deleteButton, 'title': title,}, context_instance=RequestContext(request))
	else:			
		return render_to_response('viewallpost.html', {'user' : account, 'posts': posts, 'title': title}, context_instance=RequestContext(request))

