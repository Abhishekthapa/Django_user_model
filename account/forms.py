from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        # field required to login
        fields = ('email', 'password')
    # cleans every field
    def clean(self):

        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('invalid login')


class AccountUpdateForn(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'username')
    # cleaning individual property

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                # check if account exists
                account = Account.objects.exclude(
                    pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError(
                'email "%s" is already in use.' % email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(
                    pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError(
                'username "%s" is already in use.' % username)
