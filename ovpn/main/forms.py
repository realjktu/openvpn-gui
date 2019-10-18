from django import forms

class OvpnConfigForm(forms.Form):
    config = forms.CharField(widget=forms.Textarea)
