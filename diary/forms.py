from datetime import datetime, date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import DiaryEntry, Tag


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')
            field.widget.attrs.setdefault('placeholder', field.label)


class DiaryEntryForm(forms.ModelForm):
    new_tags = forms.CharField(
        max_length=200,
        required=False,
        help_text='Add new tags separated by commas (e.g., travel, work, family)'
    )

    class Meta:
        model = DiaryEntry
        fields = ['title', 'content', 'mood', 'tags', 'created_at']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a title for your entry...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your thoughts here...'
            }),
            'mood': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': 5
            }),
            'created_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].required = False
        self.fields['new_tags'].widget.attrs.setdefault('class', 'form-control')

    def clean_created_at(self):
        value = self.cleaned_data.get('created_at')
        if value:
            # If incoming value is naive datetime-local string, convert to date comparison
            if isinstance(value, datetime):
                if value.date() > date.today():
                    raise forms.ValidationError("The date/time cannot be in the future.")
            elif isinstance(value, date):
                if value > date.today():
                    raise forms.ValidationError("The date cannot be in the future.")
        return value

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            new_tags_str = self.cleaned_data.get('new_tags', '')
            if new_tags_str:
                tag_names = [t.strip() for t in new_tags_str.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
                    instance.tags.add(tag)
            self.save_m2m()
        return instance