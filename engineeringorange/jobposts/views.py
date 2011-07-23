from engineeringorange.jobposts.models import *
from engineeringorange.messages.models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import redirect, render_to_response, get_object_or_404
import datetime

def addpost(request, userid):
	form = JobPositionForm(request.POST or None)
	form2 = JobPostForm(request.POST or None, initial={'validity': datetime.datetime.now()+datetime.timedelta(days=7)})
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
	closed=''

	#check is post has expired
	if post.validity < datetime.datetime.now():
		closed = 'this post is closed';	

	#check who's viewing the post
	result = Jobseeker.objects.filter(userid=userid).distinct()
	if result:
		form = MessageForm(request.POST or None, initial={'subject': 'Re: ' + str(post.jobid.title)})
		if request.POST and form.is_valid():
			newmsg = form.save(commit=False)
			newmsg.fromid = account
			newmsg.toid = get_object_or_404(Accounts, userid = company.userid)
			newmsg.senddate = datetime.datetime.now()
			newmsg.save()
			return render_to_response('viewpost.html', {'user': account, 'post': get_object_or_404(Jobpositions, jobid=jobid), 'qualifications' : post, 'form': MessageForm( None), 'company': company, 'closed': closed, 'sent': 'Your message has been sent!'}, context_instance=RequestContext(request))
	
	return render_to_response('viewpost.html', {'user': account, 'post': get_object_or_404(Jobpositions, jobid=jobid), 'qualifications' : post, 'form': form, 'company': company, 'closed': closed}, context_instance=RequestContext(request))

def viewall(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	return render_to_response('viewallpost.html', {'user' : account, 'posts': Jobpostings.objects.filter(userid=userid).distinct()})

def searchJobPosts(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    js = get_object_or_404(Jobseeker, userid=userid)
    form = SearchJobsForm(request.POST or None)
    if request.method == "POST":
        
        if form.is_valid():
            update = form.save(commit=False)
            update.userid = js.userid
            update.save()        
            return HttpResponseRedirect('/jobseeker/' +str(account.userid.userid))
    else:
        form = SearchJobsForm(instance = js)
        jobpos = request.GET.get('jobid', 0)
        return render_to_response("jobsearch.html/", {"user": account, "form": form, "results": jobpos},   context_instance=RequestContext(request))
   
def viewsearchresults(request, userid):
	industryid = request.GET.get('industryid', '')
	
	account = get_object_or_404(Accounts, userid=userid)
	#jobs  = Jobpositions.objects.get(industryid = industryid)
	#jobposts = jobs.jobpostings_set.all()
	#jobposts = Jobpositions.objects.filter(industryid=industryid).select_related(request.GET.get('jobid', ''))
	qset = (
            Q(industryid=industryid)
    )
	jobposts = Jobpositions.objects.filter(qset).distinct()
	print(jobposts)
	return render_to_response('jobsearchresults.html', {'user' : account, 'posts': jobposts, 'industry': industryid})