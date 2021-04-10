from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404
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


def viewemail(request):
    if request.method == 'POST':
        # data = email_data(request.POST['email'])
        data = {
            'Subject': 'Notification: Data + Blockchain Meetup with Covalent  @ Fri 9 Apr 2021 20:00 - 21:00 (IST) (anishr890@gmail.com)',
            'Date': '2021-04-09',
            'Sender': 'Google Calendar <calendar-notification@google.com>',
            'Snippet': 'Data + Blockchain Meetup with Covalent When Fri 9 Apr 2021 20:00 – 21:00 India Standard Time - Kolkata Where https://www.airmeet.com/e/e4175350-95e7-11eb-ac57-b501bd5811f6 (map) Calendar anishr890@',
            'Message_body': b'This is a notification for:\r\n\r\nTitle: Data + Blockchain Meetup with Covalent\r\nThis is an introduction to the world of data science in the blockchain  \r\nspace through Covalent, a unified API for blockchain data.\r\nPlease join the event here -  \r\nhttps://www.airmeet.com/e/e4175350-95e7-11eb-ac57-b501bd5811f6\r\nWe recommend using a laptop or a desktop computer with the Chrome browser  \r\nfor the best experience.\r\nWhen: Fri 9 Apr 2021 20:00 \xe2\x80\x93 21:00 India Standard Time - Kolkata\r\nWhere: https://www.airmeet.com/e/e4175350-95e7-11eb-ac57-b501bd5811f6\r\nCalendar: anishr890@gmail.com\r\nWho:\r\n     * LumosLabs- organiser\r\n     * anishr890@gmail.com- creator\r\n\r\nEvent details:  \r\nhttps://calendar.google.com/calendar/event?action=VIEW&eid=X2NrcTMyZHBsNmNxajBiOXA2bGlqZWI5aDY1aW00YmIxY2NxamViYjI2a28zMm9qNDZrczMyY2I2Nm8gYW5pc2hyODkwQG0&tok=MTYjaW5mb0BhaXJtZWV0LmNvbWRlMzU4NWU0N2IxZGFiY2IxOWY1NjIyY2Q3ZTBjMjNkYWI1NjRjMzI&ctz=Asia%2FKolkata&hl=en_GB&es=1\r\n\r\nInvitation from Google Calendar: https://calendar.google.com/calendar/\r\n\r\nYou are receiving this email at the account anishr890@gmail.com because you  \r\nare subscribed for notifications on calendar anishr890@gmail.com.\r\n\r\nTo stop receiving these emails, please log in to  \r\nhttps://calendar.google.com/calendar/ and change your notification settings  \r\nfor this calendar.\r\n\r\nForwarding this invitation could allow any recipient to send a response to  \r\nthe organiser and be added to the guest list, invite others regardless of  \r\ntheir own invitation status or to modify your RSVP. Learn more at  \r\nhttps://support.google.com/calendar/answer/37135#forwarding\r\n'
        }
        return render(request, 'mailit/viewemail.html', data)
    else:
        print("INVALID REQUEST")
        return Http404()
