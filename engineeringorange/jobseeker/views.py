from engineeringorange.jobseeker.models import *
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
    return render_to_response('jobseeker.html', {'jobseeker': js, 'user': account, 'announcements': Announcement.objects.filter(annType='e').distinct()[:10]})

def viewall(request, userid):
    account = get_object_or_404(Accounts, userid=userid)
    return render_to_response('inbox.html', {'user': account, 'messages': Messages.objects.filter(toid=account).distinct()[:20]})

def viewmsg(request, userid, msgid):
    account = get_object_or_404(Accounts, userid=userid)
    message = get_object_or_404(Messages, msgid=msgid)
    return render_to_response('message.html', {'user': account, 'message': message})
    