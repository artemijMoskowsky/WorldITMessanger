from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# Імпорт Клаі з текучого додатку
from .views import RegistrationView, CodeVerificationView, LoginUserView, CreatePostView, UpdatePostView, DeletePostView, PostListView, PostDetailView

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
    #  Маршрут для сторінки post_app (Створення постів)
    path('create_post/',  # URL-адреса
        CreatePostView.as_view(), # View-клас для створення постів
        name = 'create_post' # Ім'я маршруту
    ),
    path('post/', PostListView.as_view(), name = 'post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/<int:pk>/edit/', UpdatePostView.as_view(), name = 'post-edit'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name = 'post-delete'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)