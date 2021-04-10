from django import forms
# from .backend import getuseremailid


class ComposeForm(forms.Form):
    sender = forms.EmailField(
        initial='example@example.com', auto_id=True, label='Sender:'help_text='Your email address, please.', disabled=True)
    reciever = forms.EmailField(
        auto_id=True, label='Reciever', help_text='A valid email address, please.')
    cc = forms.EmailField(auto_id=True, required=False, label='CC')
    content = forms.Textarea(attrs={})
