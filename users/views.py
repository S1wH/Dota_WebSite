from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as LoginViewAuth
from .models import MyUser
from .forms import RegistrationForm


class RegistrationView(CreateView):
    model = MyUser
    success_url = reverse_lazy("mainapp:tasks")
    form_class = RegistrationForm

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


class LoginView(LoginViewAuth):
    template_name = "users/login.html"
