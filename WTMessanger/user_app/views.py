from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class RegistrationView(TemplateView):
    template_name = "registration/registration.html"

class LoginView(TemplateView):
    template_name = "login/login.html"

class CodeView(TemplateView):
    template_name = "code/code.html"

class QrcodeView(TemplateView):
    template_name = "qrcode_template/qrcode_tem.html"