from django.shortcuts import render
from .backend import getrecenthtml


def inbox(request):
    return render(request, 'mailit/inbox.html', {
        'emails': getrecenthtml(15)
    })


def test(request):
    return render(request, 'base.html')


