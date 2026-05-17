from django import forms
from django.contrib.auth import get_user_model
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegistForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels ={
            'username': 'ユーザ名',
            'email': 'メールアドレス',
            'password': 'パスワード',
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        user = User(**{k: v for k, v in self.cleaned_data.items() if k != 'password'})
        try:
            validate_password(password, user)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password



    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user