from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as LoginViewAuth
from .models import MyUser
from .forms import RegistrationForm


class RegistrationView(CreateView):
    model = MyUser
    success_url = reverse_lazy("usersapp:login")
    form_class = RegistrationForm


class LoginView(LoginViewAuth):
    template_name = "users/login.html"
