from engineeringorange.messages.models import *
from engineeringorange.resume.models import *
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, get_object_or_404
import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def viewall(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	messages = Messages.objects.filter(toid=account).distinct().order_by('senddate').reverse()	
	return render_to_response('inbox.html', {'user': account, 'messages': messages}, context_instance=RequestContext(request))

@login_required
def sent(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	messages = Messages.objects.filter(fromid=account).distinct().order_by('senddate').reverse()	
	return render_to_response('inbox.html', {'user': account, 'messages': messages, 'sent': account}, context_instance=RequestContext(request))
	
@login_required
def viewmsg(request, userid, msgid):
	account = get_object_or_404(Accounts, userid=userid)
	message = get_object_or_404(Messages, msgid=msgid)
	fromUser = Messages.objects.filter(fromid = account.userid, msgid = msgid)
	toUser = Messages.objects.filter(toid = account.userid, msgid = msgid)
	replyButton = BlankMessageForm(request.POST or None)
	deleteButton = BlankMessageForm(request.POST or None)
	if fromUser or toUser:	
		if toUser:
			message.readdate = datetime.datetime.now()
			message.save()
		return render_to_response('message.html', {'user': account, 'message': message, 'delete': deleteButton}, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/messages/' + str(account.userid))			

@login_required
def reply(request, userid, msgid):
	account = get_object_or_404(Accounts, userid=userid)
	message = get_object_or_404(Messages, msgid=msgid)
	form = MessageForm(request.POST or None, initial={'subject': 'RE: '+ str(message.subject)})

	to = message.fromid
	sender = message.toid
	if account == get_object_or_404(Accounts, email= message.fromid):
		to = message.toid
		sender = message.fromid

	if account == get_object_or_404(Accounts, email = sender):
		if request.POST and form.is_valid() :
			newmsg = form.save(commit=False)
			newmsg.fromid = account
			newmsg.toid = get_object_or_404(Accounts, email = to)
			newmsg.senddate = datetime.datetime.now()
			newmsg.save()
			return HttpResponseRedirect('/message/'+ str(account.userid) +'/' +str(newmsg.msgid))
		else:		
			return render_to_response('createmessage.html/', {'form': form, 'user' : account}, context_instance=RequestContext(request))
	return HttpResponseRedirect('/messages/' + str(account.userid))

@login_required
def delete(request, userid, msgid):
	account = get_object_or_404(Accounts, userid=userid)		
	if request.POST:
		message = get_object_or_404(Messages, msgid=msgid)
		message.delete()
		if account == get_object_or_404(Accounts, email = message.fromid):
			return HttpResponseRedirect('/messages/sent/' + str(account.userid))
	return HttpResponseRedirect('/messages/' + str(account.userid))

@login_required
def compose(request, userid):
	account = get_object_or_404(Accounts, userid=userid)
	result = Jobseeker.objects.filter(userid=userid).distinct()
	if result:
		form = SeekerMessageForm(request.POST or None)
	else:
		form = EmployerMessageForm(request.POST or None)
	if request.POST and form.is_valid():
			newmsg = form.save(commit=False)
			newmsg.fromid = account
			newmsg.senddate = datetime.datetime.now()
			newmsg.save()
			return HttpResponseRedirect('/message/'+ str(account.userid) +'/' +str(newmsg.msgid))

	return render_to_response('createmessage.html/', {'form': form, 'user' : account}, context_instance=RequestContext(request))

