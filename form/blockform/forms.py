from django import forms


class HomeForm(forms.Form):
    post = forms.CharField(label='Bitcoin Address')
    dateFrom = forms.DateField(label='From date (e.g. 2010-05-20):', required=False)
    dateTo = forms.DateField(label='To date (e.g. 2010-05-20):', required=False)
