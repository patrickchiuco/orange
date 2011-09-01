from engineeringorange.employer.models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def sendpassword(request):
    email = request.GET.get('email', '')

    # generate a new password
    result = 'hello'
    while result:
        password = str(random.randint(0,10000000000))
        result = get_object_or_404(User, password = password)
    
    subject = 'Engineering Orange: Your New Password'
    message = 'The password for your account is: ' + password + '. Please access your account and change the password immediately.'

    if email:
        try:
            #place new password
            result.password = password
            result.save()
            send_mail(subject, message, 'engineeringorange@gmail.com', [email])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect("/")
    else:
        return HttpResponse('The email entered does not have a corresponding account. Create an account for Orange now!')

