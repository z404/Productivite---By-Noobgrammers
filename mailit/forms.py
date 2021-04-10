from django import forms
from .backend import getuseremailid


class ComposeForm(forms.Form):
    sender = forms.EmailField(initial=getuseremailid(), label='Sender:', disabled=True)
    receiver = forms.EmailField(label='Receiver')
    subject = forms.CharField(max_length=120, label = "Subject")
    #cc = forms.EmailField( required=False, label='CC')
    message = forms.CharField(widget=forms.Textarea(attrs={"name":"message"}))
