from django.shortcuts import render, HttpResponseRedirect
from .backend import getrecenthtml, sendemail


def inbox(request):
    return render(request, 'mailit/inbox.html', {
        'emails': getrecenthtml(15)
    })


def test(request):
    return render(request, 'mailit/base.html')

def compose(request):
    if request.method == 'POST':
        sender = request.POST['sender']
        to = request.POST['to']
        subject = request.POST['subject']
        message = request.POST['message']
        ret = sendemail(sender, to, subject, message)
        if ret[0] == True:
            return HttpResponseRedirect("inbox")
        elif ret[0] == False:
            print(ret)