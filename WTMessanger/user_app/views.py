from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegistrationForm, CodeVerificationForm, LoginForm
from .models import WTUser
from django.contrib.auth.views import LoginView
import random, string 

class RegistrationView(FormView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('register-verify')
    
    def form_valid(self, form):
        self.request.session['registration_data'] = {
            'username': form.cleaned_data['username'],
            'email': form.cleaned_data['email'],
            'password': form.cleaned_data['password'],
        }
        
        code = ''.join(random.choices(string.digits, k=6))
        self.request.session['verification_code'] = code
        
        send_mail(
            subject='Код підтвердження реєстрації',
            message=f'Ваш код підтвердження: {code}',
            from_email=None,
            recipient_list=[form.cleaned_data['email']],
            fail_silently=False,
        )
        
        messages.success(self.request, 'Код підтвердження відправлено на ваш email')
        return super().form_valid(form)



class LoginUserView(LoginView):
    template_name = 'login/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    next_page = reverse_lazy('core')

    # def form_valid(self, form):
    #     # Добавляем отладочную информацию
    #     print(f"Аутентифицируем пользователя: {form.get_user()}")
    #     return super().form_valid(form)
class CodeVerificationView(FormView):
    template_name = 'code/code.html'
    form_class = CodeVerificationForm
    success_url = reverse_lazy('core')
    
    def dispatch(self, request, *args, **kwargs):
        if 'registration_data' not in request.session:
            return redirect('register')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user_code = form.cleaned_data['full_code']
        saved_code = self.request.session.get('verification_code')
        
        if user_code != saved_code:
            for field in ['code_1', 'code_2', 'code_3', 'code_4', 'code_5', 'code_6']:
                form.add_error(field, '')
            form.add_error(None, 'Невірний код підтвердження')
            return self.form_invalid(form)
        
        registration_data = self.request.session['registration_data']
        user = WTUser.objects.create_user(
            username=registration_data['username'], # Сносить при обновлении модели
            email=registration_data['email'],
            password=registration_data['password']
        )
        
        login(self.request, user)
        
        for key in ['registration_data', 'verification_code']:
            if key in self.request.session:
                del self.request.session[key]
        
        messages.success(self.request, 'Реєстрація успішно завершена!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.request.session['registration_data']['email']
        context['code_range'] = range(1, 7)
        return context
