from django import forms


class RequestForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)  # the title of the request
    location = forms.CharField(max_length=50)  # the location of the tutee (as specified by the tutee)
    pub_date = forms.DateTimeField()  # when it was published
    description = forms.CharField(max_length=1000)  # a description written by the tutee