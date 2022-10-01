from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm


class BoardForm(forms.ModelForm):
    class Meta:
        model = BoardNotice
        fields = [
            'title',
            'text',
            'category'
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")
        if title is None:
            raise forms.ValidationError(
                "Title cannot be empty"
            )
        if text is not None and len(text) < 20:
            raise forms.ValidationError(
                "Text must be at least 20 characters long."
            )
        return cleaned_data


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['response_user', 'text', 'response_to']


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2",)


class OneTimeForm(forms.ModelForm):
    class Meta:
        model = OneTimeCode
        fields = ['code']

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get("code")

        if not OneTimeCode.objects.filter(code=code).exists():
            raise forms.ValidationError(
                "Wrong code"
            )
        return cleaned_data


class MassMailForm(forms.ModelForm):
    class Meta:
        model = MassMail
        fields = ['title', 'text']
