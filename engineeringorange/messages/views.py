from engineeringorange.messages.models import *
from engineeringorange.resume.models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, get_object_or_404
import datetime

# Create your views here.
def viewall(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	return render_to_response('inbox.html', {'user': account, 'messages': Messages.objects.filter(toid=account).distinct()[:20]})

def viewsent(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	return render_to_response('inbox.html', {'user': account, 'messages': Messages.objects.filter(fromid=account).distinct()[:20]})

def viewmsg(request, userid, msgid):
	account = get_object_or_404(Accounts, userid=userid)
	message = get_object_or_404(Messages, msgid=msgid)
	result = Messages.objects.filter(toid = account.userid, msgid = msgid)
	if result:
		message.readdate = datetime.datetime.now()
		message.save()
	return render_to_response('message.html', {'user': account, 'message': message})

def reply(request, userid, msgid):
	account = get_object_or_404(Accounts, userid=userid)
	message = get_object_or_404(Messages, msgid=msgid)
	form = MessageForm(request.POST or None, initial={'fromid': account, 'toid': message.fromid, 'subject': 'RE: ' + message.subject})
	
	if request.POST and form.is_valid():
		newmsg = form.save(commit=False)
		newmsg.senddate = datetime.datetime.now()
		newmsg.save()
		return HttpResponseRedirect('/message/'+ str(account.userid) +'/' +str(newmsg.msgid))
	
	return render_to_response('createmessage.html/', {'form': form, 'user' : account}, context_instance=RequestContext(request))

def delete(request, userid, msgid):
	account = get_object_or_404(Accounts, userid=userid)
	message = get_object_404(Messages, msgid=msgid)
	message.delete
	return HttpResponseRedirect('/messages/' + str(account.userid))

