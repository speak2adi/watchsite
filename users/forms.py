from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class UserRegistration(UserCreationForm):
    class Meta:
        models = CustomUser
        fields = ('name', 'email')


class UserChange(UserChangeForm):
    class Meta:
        models = CustomUser
        fields = ('name', 'email')


