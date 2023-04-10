from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import MyUser


class RegistrationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password1', 'password2')