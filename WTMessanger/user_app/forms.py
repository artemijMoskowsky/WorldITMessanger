'''
   forms.py Безпечно обробляє дані від користувачів.

   forms.py Спрощує валідацію та збереження даних.

   forms.py Дозволяє повторно використовувати форми у різних частинах сайту.
'''



from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


# Форма для реєстрації нового користувача, успадкована від ModelForm
class RegistrationForm(forms.ModelForm):
    # Поле для паролю з валідацією та стилізацією
    password = forms.CharField(
        widget = forms.PasswordInput(attrs={'class': 'form-control'}),  # Використання PasswordInput для приховання паролю
        label = 'Пароль',  # Назва поля
        validators=[validate_password]  # Валідатор для перевірки складності паролю
    )
    
    # Поле для підтвердження паролю
    password2 = forms.CharField(
        widget = forms.PasswordInput(attrs={'class': 'form-control'}),  # Аналогічний віджет
        label = 'Підтвердження паролю'  # Назва поля
    )
    
    # Клас Meta визначає модель та додаткові налаштування форми
    class Meta:
        model = User  # Використовуємо вбудовану модель User
        fields = ['username', 'email', 'password']  # Поля, які відображаються у формі
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),  # Стилізація поля username
            'email': forms.EmailInput(attrs={'class': 'form-control'}),  # Стилізація поля email
        }
        labels = {
            'username': "Ім'я користувача",  # Українська мітка для поля username
            'email': 'Email'  # Мітка для поля email
        }
    
    # Метод для перевірки унікальності email
    def clean_email(self):
        email = self.cleaned_data.get('email')  # Отримуємо email з форми
        if User.objects.filter(email=email).exists():  # Перевіряємо, чи існує такий email у базі
            raise ValidationError("Цей email вже зареєстрований!")  # Викидаємо помилку, якщо email зайнятий
        return email  # Повертаємо email, якщо все добре
    
    # Загальний метод для перевірки форми 
    def clean(self):
        cleaned_data = super().clean()  # Отримуємо "очищені" дані форми
        password = cleaned_data.get('password')  # Отримуємо пароль
        password2 = cleaned_data.get('password2')  # Отримуємо підтвердження паролю
        
        # Перевіряємо, чи паролі співпадають
        if password and password2 and password != password2:
            self.add_error('password2', 'Паролі не співпадають')  # Додаємо помилку до поля password2
        
        return cleaned_data  # Повертаємо дані форми


# Форма для введення коду підтвердження (email верифікації)
class CodeVerificationForm(forms.Form):
    code = forms.CharField(
        label = 'Код підтвердження',  # Назва поля
        max_length = 6,  # Максимальна довжина коду
        min_length = 6,  # Мінімальна довжина коду
        widget = forms.TextInput(attrs={
            'class': 'form-control',  # Стилізація поля
            'placeholder': 'Введіть шестизначний код'  # Підказка для користувача
        })
    )