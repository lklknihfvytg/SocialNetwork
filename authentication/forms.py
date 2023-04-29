from django import forms
from network.models import Profile
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    # required_css_class = "field"

    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get('username')
    #     password = cleaned_data.get('password')
    #
    #     try:
    #         self.user = User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         raise forms.ValidationError(f'Логин неверный!')
    #
    #     if not self.user.check_password(password):
    #         raise forms.ValidationError(f'Пароль неверный!')


# class RegisterForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['email'].required = True
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')
#         widgets = {'password': forms.PasswordInput()}


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'surname', 'about', 'city', 'date_of_birth', 'profile_pic')
