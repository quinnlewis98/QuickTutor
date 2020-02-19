from django import forms


class RequestForm(forms.Form):
    '''suggestion_name = forms.CharField(label='Name', max_length=50,
                                      widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', max_length=300,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))'''

    # should have something for each field defined in the request model