from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from pyhunter import PyHunter
import clearbit

hunter = PyHunter('bdb76854417615a762ba0986754e3eabfd7998eb')
clearbit.key = "sk_ec043898c30b64120ad73115754e52bd"


def check_mail(mail):
    try:
        # status = {'result': 'good'}
        status = hunter.email_verifier(mail)
        if status.get('result') == "undeliverable":
            return False
        else:
            return True
    except:
        return False

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", 'first_name', 'last_name')
        widgets = {'first_name': forms.HiddenInput(), 'last_name': forms.HiddenInput()}


    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')

        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        else:
            if check_mail(email):
                return email
            else:
                raise forms.ValidationError("Enter good email")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        try:
            lookup = clearbit.Enrichment.find(email=user.email, stream=True)

            if 'person' in lookup:
                user.first_name = lookup['person']['name']['givenName']
                user.last_name = lookup['person']['name']['familyName']
            else:
                user.first_name = ''
                user.last_name = ''
        except:
            user.first_name = ''
            user.last_name = ''

        if commit:
            user.save()
        return user

