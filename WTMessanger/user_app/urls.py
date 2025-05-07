from django.urls import path
from .views import RegistrationView, LoginView, QrcodeView, CodeView

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name = 'reg'),
    path("login/", LoginView.as_view(), name = 'login'),
    path("user_qrcode/", QrcodeView.as_view(), name = 'qrcode'),
    path("user_code/", CodeView.as_view(), name = 'code')
]