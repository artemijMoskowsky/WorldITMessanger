'''
   forms.py Безпечно обробляє дані від користувачів.

   forms.py Спрощує валідацію та збереження даних.

   forms.py Дозволяє повторно використовувати форми у різних частинах сайту.
'''





from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import WTUser 


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget = forms.PasswordInput(attrs = {'class': 'data-input img'}),
        label ='Пароль',
        validators=[validate_password]
    )
    
    password2 = forms.CharField(
        widget = forms.PasswordInput(attrs = {'class': 'data-input img'}),
        label = 'Підтвердження паролю'
    )
    
    class Meta:
        model = WTUser  
        fields = ['username', 'email', 'password']  
        widgets = {
            'username': forms.TextInput(attrs = {'class': 'data-input noimg'}),
            'email': forms.EmailInput(attrs = {'class': 'data-input noimg'}),
        }
        labels = {
            'username': "Ім'я користувача",
            'email': 'Email'
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if WTUser.objects.filter(email=email).exists():  
            raise ValidationError("Цей email вже зареєстрований!")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password and password2 and password != password2:
            self.add_error('password2', 'Паролі не співпадають')
        
        return cleaned_data


class LoginForm(AuthenticationForm):
    # username = forms.CharField(
    #     label="Логин или Email",
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'autocomplete': 'username'
    #     })
    # )
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        # self.fields["username"].label = "Логин или Email"
        self.fields["username"].widget.attrs.update({"class": "data-input noimg"})
        self.fields["password"].widget.attrs.update({"class": "data-input img"})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            WTUser.objects.get(username = username)
            return username
        except:
            try:
                user = WTUser.objects.get(email = username)
                return user.username
            except:
                raise ValidationError("Користувача с таким ім'ям або поштою не існує")

        # return self.cleaned_data

class CodeVerificationForm(forms.Form):
    code_1 = forms.CharField(
        label='',
        max_length = 1,
        min_length = 1,
        widget=forms.TextInput(attrs = {
            'class': 'number-code',
            'placeholder': '',
            'maxlength': '1',
            'autocomplete': 'off'
        })
    )
    code_2 = forms.CharField(
        label = '',
        max_length = 1,
        min_length = 1,
        widget=forms.TextInput(attrs = {
            'class': 'number-code',
            'placeholder': '',
            'maxlength': '1',
            'autocomplete': 'off'
        })
    )
    code_3 = forms.CharField(
        label = '',
        max_length = 1,
        min_length = 1,
        widget = forms.TextInput(attrs = {
            'class': 'number-code',
            'placeholder': '',
            'maxlength': '1',
            'autocomplete': 'off'
        })
    )
    code_4 = forms.CharField(
        label = '',
        max_length = 1,
        min_length = 1,
        widget=forms.TextInput(attrs = {
            'class': 'number-code',
            'placeholder': '',
            'maxlength': '1',
            'autocomplete': 'off'
        })
    )
    code_5 = forms.CharField(
        label = '',
        max_length = 1,
        min_length = 1,
        widget = forms.TextInput(attrs = {
            'class': 'number-code',
            'placeholder': '',
            'maxlength': '1',
            'autocomplete': 'off'
        })
    )
    code_6 = forms.CharField(
        label = '',
        max_length = 1,
        min_length = 1,
        widget = forms.TextInput(attrs = {
            'class': 'number-code',
            'placeholder': '',
            'maxlength': '1',
            'autocomplete': 'off'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        code_parts = [
            cleaned_data.get('code_1'),
            cleaned_data.get('code_2'),
            cleaned_data.get('code_3'),
            cleaned_data.get('code_4'),
            cleaned_data.get('code_5'),
            cleaned_data.get('code_6')
        ]
        full_code = ''.join(code_parts)
        
        if None in code_parts or '' in code_parts:
            raise forms.ValidationError("Усі поля мають бути заповнені")
        
        if not full_code.isdigit():
            raise forms.ValidationError("Код повинен містити лише цифри")
        
        if len(full_code) != 6:
            raise forms.ValidationError("Код має складатися із 6 цифр")
        
        cleaned_data['full_code'] = full_code
        
        return cleaned_data