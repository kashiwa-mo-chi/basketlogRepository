from django import forms
from django.contrib.auth import get_user_model
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegistForm(forms.ModelForm):

    password_confirm = forms.CharField(
        label='パスワード(再入力)',
        widget=forms.PasswordInput()
    )

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
        help_texts = {
            'password': '英数字を含む８文字以上',
        }

        error_messages = {
            'email': {
                'unique': 'このメールアドレスはすでに登録されています',
            },
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if password:
            if len(password) < 8:
                raise forms.ValidationError(
                    'パスワードは英数字を含む8文字以上で設定してください。'
                )

            if not any(c.isalpha() for c in password):
                raise forms.ValidationError(
                    'パスワードには英字を1文字以上含めてください。'
                )

            if not any(c.isdigit() for c in password):
                raise forms.ValidationError(
                    'パスワードには数字を1文字以上含めてください。'
                )

        user = User(
            **{k: v for k, v in self.cleaned_data.items()
            if k not in ['password', 'password_confirm']
            })

        try:
            validate_password(password, user)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)

        return password

    def clean(self):
        cleaned_data = super().clean()

        password = self.data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:
            if password != password_confirm:
                self.add_error(
                    'password_confirm',
                    'パスワードが一致しません。'
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
        labels = {
            "email":"メールアドレス",
        }


    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に使用されています")
        
        return email

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]
        labels = {
            "username": "ユーザ名",
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)

        self.initial["username"] = ""

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("このユーザ名は既に使用されています")
        
        return username