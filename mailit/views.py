from django.shortcuts import render, HttpResponseRedirect
from .backend import getrecenthtml, sendemail, getuseremailid
from .forms import ComposeForm


def inbox(request):
    return render(request, "mailit/inbox.html", {"emails": getrecenthtml(15)})


def test(request):
    return render(request, "mailit/base.html")


def compose(request):
    if request.method == "POST":
        # sender = request.POST['sender']
        receiver = request.POST["receiver"]
        subject = request.POST["subject"]
        message = request.POST["message"]
        ret = sendemail(getuseremailid(), receiver, subject, message)
        if ret[0] == True:
            return HttpResponseRedirect("../inbox")
        elif ret[0] == False:
            print(ret)
    elif request.method == "GET":
        return render(request, "mailit/compose.html", {"form": ComposeForm()})
