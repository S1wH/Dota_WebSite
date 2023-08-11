from django.contrib.auth.forms import UserCreationForm

from mainapp.models import QueueTask
from .models import MyUser
from mainapp.tasks import send_email


class RegistrationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ("username", "email", "password1", "password2")

    def send_mail(self):
        email = self.cleaned_data['email']
        result = send_email.delay(email)
        QueueTask.objects.create(
            task_id=result.id,
            name=f'Sending email to {email}',
        )
