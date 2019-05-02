from django import forms


class ContactForm(forms.Form):
    contact_name = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'input'})
    )
    contact_email = forms.EmailField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'input'}))
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'textarea'})
    )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Dit navn:"
        self.fields['contact_email'].label = "Din email-adresse:"
        self.fields['content'].label = "Din besked:"
