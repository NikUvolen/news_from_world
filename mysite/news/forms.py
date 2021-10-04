import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Category, News


# class NewsForm(forms.Form):
#     title = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
#     content = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
#     is_published = forms.BooleanField(initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
#     category = forms.ModelChoiceField(Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'photo', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'photo': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('The name must not begin with a number')
        return title


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='User name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password input', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def is_valid(self):
        result = super().is_valid()
        for x in self.fields:
            attrs = self.fields[x].widget.attrs
            if ("__all__" in self.errors) or (x in self.errors):
                error_css_class = 'is-invalid'
            else:
                error_css_class = 'is-valid'
            attrs.update({'class': attrs.get('class', '') + ' ' + error_css_class})
        return result

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='User name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password input', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
