from django import forms

class TopicSearchForm(forms.Form):
    title = forms.CharField(label='Topic title',widget=forms.Textarea())