from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUP(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    first_name = forms.CharField(min_length=3, max_length=20, required=True)
    password = forms.CharField(min_length=8, max_length=100, required=True)
    repeat_password = forms.CharField(max_length=100, required=True)

    def clean_email(self):
        if User.objects.filter(username=self.cleaned_data.get('email')).exists():
            raise ValidationError('User is exists')
        return self.cleaned_data.get('email')

    def clean_repeat_password(self):
        if self.cleaned_data.get('repeat_password') != self.cleaned_data.get('password'):
            raise ValidationError('Repate password is wrong!')
        return self.cleaned_data.get('repeat_password')


class Login(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(min_length=8, max_length=100, required=True)


class Profile(forms.Form):
    image = forms.ImageField(required=False)
    first_name = forms.CharField(min_length=3, max_length=20, required=True)

    def clean_image(self):
        if self.cleaned_data.get('image'):
            if self.cleaned_data.get('image').size > 5242880:
                raise ValidationError('Maximum size image is 5MB')
        return self.cleaned_data['image']


class Change_password(forms.Form):
    old_password = forms.CharField(max_length=100, required=True)
    new_password = forms.CharField(min_length=8, max_length=100, required=True)
    repeat_password = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        if not self._user.check_password(self.cleaned_data.get('old_password')):
            raise ValidationError('Old password is wrong')
        return self.cleaned_data['old_password']

    def clean_repeat_password(self):
        if self.cleaned_data.get('repeat_password') != self.cleaned_data.get('new_password'):
            raise ValidationError('Repeat password is wrong')
