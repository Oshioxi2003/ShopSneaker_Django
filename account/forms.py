from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms.widgets import PasswordInput, TextInput


# Registeration form
class CreationUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def __init__(self, *args, **kwargs):

        super(CreationUserForm, self).__init__(*args, **kwargs)


        self.fields['email'].required = True

    # Email validation

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError('This email is invalid')
        
        if len(email) >= 350:

            raise forms.ValidationError("Your email is too long")
        
        return email
    


# Login form

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


#update form

class UpdateUserForm(forms.ModelForm):

    password = None

    def __init__(self, *args, **kwargs):

        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['email'].required = True


    # Email validation

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():

            raise forms.ValidationError('This email is invalid')
        
        if len(email) >= 350:

            raise forms.ValidationError("Your email is too long")
        
        return email

    class Meta:

        model = User

        fields = ['username', 'email']
        exclude = ['password1', 'password2']