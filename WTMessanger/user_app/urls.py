from django.urls import path
# Імпорт Клаі з текучого додатку
from .views import RegistrationView, CodeVerificationView, LoginUserView, UserLogoutView, CreatePostView

# Визначаємо список URL-шляхів (маршрутів) додатку
urlpatterns = [
    # Маршрут для сторінки реєстрації
    path(
        'register/',  # URL-адреса
        RegistrationView.as_view(),  # View-клас, що обробляє цей маршрут
        name='register'  # Унікальне ім'я маршруту для зворотних посилань
    ),
    
    # Маршрут для сторінки верифікації коду після реєстрації
    path(
        'register/verify/',  # URL-адреса (відносний шлях)
        CodeVerificationView.as_view(),  # View-клас для верифікації
        name='register-verify'  # Ім'я маршруту
    ),
    
    # Маршрут для сторінки входу (авторизації)
    path(
        'login/',  # URL-адреса
        LoginUserView.as_view(),  # View-клас для авторизації
        name='login'  # Ім'я маршруту
    ),
    path(
        'logout/',
        UserLogoutView.as_view(),
        name="logout"
    ),
    #  Маршрут для сторінки post_app (Створення постів)
    path('create/',  # URL-адреса
        CreatePostView.as_view(), # View-клас для створення постів
        name = 'create_post' # Ім'я маршруту
    )
]