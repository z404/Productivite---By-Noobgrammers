from django.shortcuts import render
from .backend import getrecent


def inbox(request):
    return render(request, 'mailit/inbox.html', {
        'emails': getrecent(10)
    })

