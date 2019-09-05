from django import forms
from django.core.exceptions import ValidationError
from .models import *


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['title', 'slug']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'slug': forms.TextInput(attrs={'class': 'form-control'})}

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We have "{}" slug already'.format(new_slug))
        return new_slug


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'slug': forms.TextInput(attrs={'class': 'form-control'}),
                   'body': forms.Textarea(attrs={'class': 'form-control'}),
                   'tags': forms.SelectMultiple(attrs={'class': 'form-control'})}

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        return new_slug


class LoginForm(forms.Form):
    login = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(
        max_length=30, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_login(self):
        input_login = self.cleaned_data['login']
        if User.objects.filter(username=input_login).count():
            raise ValidationError('Неверный пароль!')
        else:
            raise ValidationError('Неверный логин!')
        return input_login


class UzForm(forms.ModelForm):

    class Meta:
        model = Use
        fields = [
            'surname', 'name', 'patronymic', 'gender', 'birthday', 'marital_status', 'address', 'phone',
            'email', 'school', 'avatar'
        ]

        widgets = {
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0975865820'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),

        }

    def clean_phone(self):
        input_phone = self.cleaned_data['phone']
        if Use.objects.filter(phone=input_phone).count():
            raise ValidationError('Такой номер телефона уже есть!')
        return input_phone

    def clean_email(self):
        input_email = self.cleaned_data['email']
        if Use.objects.filter(email=input_email).count():
            raise ValidationError('Такой email уже есть!')
        return input_email
