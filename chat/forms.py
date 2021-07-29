from django import forms
from django.db import models
from django.db.models import fields
from .models import Profile, ChatRoomPublic
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','last_name','first_name')


class ChatRoomPublicForm(forms.ModelForm):
    class Meta:
        model = ChatRoomPublic
        fields = '__all__'