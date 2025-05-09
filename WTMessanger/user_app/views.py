from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegistrationForm, CodeVerificationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
import random, string 

class RegistrationView(FormView):
    """
    View для обробки реєстрації нового користувача.
    Використовує RegistrationForm для валідації даних.
    """
    template_name = 'registration/register.html'  # Шаблон сторінки реєстрації
    form_class = RegistrationForm  # Форма, яка використовується
    success_url = reverse_lazy('register-verify')  # Куди перенаправляти при успіху
    
    def form_valid(self, form):
        """
        Обробка коректно заповненої форми.
        1. Зберігає дані реєстрації в сесії
        2. Генерує та відправляє код підтвердження
        """
        # Зберігаємо дані форми в сесії для подальшого використання
        self.request.session['registration_data'] = {
            'username': form.cleaned_data['username'],
            'email': form.cleaned_data['email'],
            'password': form.cleaned_data['password'],
        }
        
        # Генеруємо 6-значний цифровий код
        code = ''.join(random.choices(string.digits, k = 6))
        self.request.session['verification_code'] = code
        
        # Відправляємо код на email користувача
        send_mail(
            subject = 'Код підтвердження реєстрації',
            message = f'Ваш код підтвердження: {code}',
            from_email = None,  # Використовується EMAIL_HOST_USER з settings.py
            recipient_list = [form.cleaned_data['email']],
            fail_silently = False,
        )
        
        # Повідомлення про успішну відправку коду
        messages.success(self.request, 'Код підтвердження відправлено на ваш email')
        return super().form_valid(form)

class LoginUserView(LoginView):
    """
    Стандартний View для авторизації користувача.
    Наслідує вбудований LoginView Django.
    """
    template_name = 'login/login.html'  # Шаблон сторінки входу
    redirect_authenticated_user = True  # Авторизованих користувачів перенаправляємо
    next_page = reverse_lazy('home')  # Куди перенаправляти після успішного входу

class CodeVerificationView(FormView):
    """
    View для підтвердження реєстрації через код з email.
    """
    template_name = 'registration/code_verify.html'  # Шаблон сторінки підтвердження
    form_class = CodeVerificationForm  # Форма з полем для коду
    success_url = reverse_lazy('home')  # Перенаправлення після успіху
    
    def dispatch(self, request, *args, **kwargs):
        """
        Перевіряємо, чи є дані реєстрації в сесії.
        Якщо ні - перенаправляємо на сторінку реєстрації.
        """
        if 'registration_data' not in request.session:
            return redirect('register')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """
        Перевіряє код підтвердження та створює користувача.
        """
        user_code = form.cleaned_data['code']  # Код від користувача
        saved_code = self.request.session.get('verification_code')  # Код з сесії
        
        # Перевіряємо збіг кодів
        if user_code != saved_code:
            form.add_error('code', 'Невірний код підтвердження')
            return self.form_invalid(form)
        
        # Отримуємо дані реєстрації з сесії
        registration_data = self.request.session['registration_data']
        
        # Створюємо нового користувача
        user = User.objects.create_user(
            username = registration_data['username'],
            email = registration_data['email'],
            password = registration_data['password']
        )
        
        # Авторизуємо користувача
        login(self.request, user)
        
        # Очищуємо сесію від тимчасових даних
        for key in ['registration_data', 'verification_code']:
            if key in self.request.session:
                del self.request.session[key]
        
        # Повідомлення про успішну реєстрацію
        messages.success(self.request, 'Реєстрація успішно завершена!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """
        Додає email у контекст шаблону для відображення.
        """
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session['registration_data']['email']
        return context