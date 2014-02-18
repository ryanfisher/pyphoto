from django import forms

class PhotoUploadForm(forms.Form):
    file = forms.FileField()
