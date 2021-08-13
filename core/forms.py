from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext as _

UserModel = get_user_model()


class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=15)
    username = forms.EmailField(label=_("Email"), required=True,
                                widget=forms.EmailInput(attrs={'autocomplete': 'true'}))
    image = forms.ImageField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Username', initial="", widget=forms.EmailInput(attrs={'autocomplete': 'true'}))
    password = forms.CharField(min_length=6,
                               label=_("Password"),
                               strip=False, initial="",
                               widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}))
    remember_me = forms.BooleanField(initial=True, required=False)
