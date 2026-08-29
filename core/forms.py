from django import forms

SERVICE_CHOICES = [
    ('', "Select a service package you're interested in..."),
    ('web-development', 'Web Development'),
    ('consulting', 'Consulting'),
    ('other', 'Other'),
]

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    service = forms.ChoiceField(choices=SERVICE_CHOICES, required=False)
    message = forms.CharField(widget=forms.Textarea)